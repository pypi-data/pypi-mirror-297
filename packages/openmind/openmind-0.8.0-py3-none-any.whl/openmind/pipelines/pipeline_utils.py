# Copyright (c) 2024 Huawei Technologies Co., Ltd.
# Copyright 2018 The HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
from typing import Any, Dict, Optional, Tuple, Union
from ..utils.hub import OpenMindHub
from ..utils import logging
from ..utils.patch_utils import _apply_patches
from ..utils.exceptions import FrameworkNotSupportedError
from ..pipelines.pipeline_registry import PipelineRegistry
from ..utils.generic import replace_invalid_characters


SUPPORTED_FRAMEWORKS = ("pt", "ms")
PIPELINE_REGISTRY = PipelineRegistry()

logger = logging.get_logger()


def pipeline_patch(change_dict=None):
    # Pipeline task patch
    import copy
    import transformers
    from transformers import AutoModel
    from transformers.pipelines import SUPPORTED_TASKS, TASK_ALIASES, PIPELINE_REGISTRY
    from transformers.pipelines.base import PipelineRegistry
    from .chatglm_pipeline import ChatGLMPipeline

    ori_supported_tasks = copy.deepcopy(SUPPORTED_TASKS)
    ori_pipeline_registry = copy.deepcopy(PIPELINE_REGISTRY)
    PATCHED_SUPPORTED_TASKS = copy.deepcopy(SUPPORTED_TASKS)
    PATCHED_SUPPORTED_TASKS["chat"] = {"impl": ChatGLMPipeline, "pt": (AutoModel,)}
    for key in PATCHED_SUPPORTED_TASKS.keys():
        if key in change_dict.keys():
            PATCHED_SUPPORTED_TASKS[key]["default"] = change_dict[key]
        else:
            PATCHED_SUPPORTED_TASKS[key]["default"] = {}
    PATCHED_PIPELINE_REGISTRY = PipelineRegistry(supported_tasks=PATCHED_SUPPORTED_TASKS, task_aliases=TASK_ALIASES)
    patch_list = [
        ("SUPPORTED_TASKS", PATCHED_SUPPORTED_TASKS),
        ("PIPELINE_REGISTRY", PATCHED_PIPELINE_REGISTRY),
    ]
    _apply_patches(patch_list, transformers.pipelines)
    return ori_supported_tasks, ori_pipeline_registry


def _get_default_model_and_revision(
    targeted_task: Dict, framework: Optional[str], task_options: Optional[Any]
) -> Union[str, Tuple[str, str]]:
    defaults = targeted_task["default"]
    if task_options:
        if task_options not in defaults:
            raise ValueError(
                replace_invalid_characters(f"The task does not provide any default models for options {task_options}")
            )
        default_models = defaults[task_options]["model"]
    elif "model" in defaults:
        default_models = targeted_task["default"]["model"]
    else:
        raise ValueError('The task defaults can\'t be correctly selected. You probably meant "translation_XX_to_YY"')

    if framework is None:
        framework = "pt"

    if framework not in SUPPORTED_FRAMEWORKS:
        raise FrameworkNotSupportedError(framework=framework)

    return default_models[framework]


def check_task(task: str) -> Tuple[str, Dict, Any]:
    return PIPELINE_REGISTRY.check_task(task)


def download_from_repo(repo_id, revision=None, cache_dir=None, force_download=False):
    if not os.path.exists(repo_id):
        local_path = OpenMindHub.snapshot_download(
            repo_id,
            revision=revision,
            cache_dir=cache_dir,
            force_download=force_download,
        )
    else:
        local_path = repo_id
    return local_path


def get_task_from_readme(model_name) -> Optional[str]:
    """
    Get the task of the model by reading the README.md file.
    """
    readme_file = os.path.join(model_name, "README.md")
    task = None
    if os.path.exists(readme_file):
        with open(readme_file, "r") as file:
            content = file.read()
            pipeline_tag = re.search(r"pipeline_tag:\s?(([a-z]*-)*[a-z]*)", content)
            if pipeline_tag:
                task = pipeline_tag.group(1)
            else:
                logger.warning("Cannot infer the task from the provided model, please provide the task explicitly.")
    else:
        logger.warning("README.md not found in the model path, please provide the task explicitly.")
    return task
