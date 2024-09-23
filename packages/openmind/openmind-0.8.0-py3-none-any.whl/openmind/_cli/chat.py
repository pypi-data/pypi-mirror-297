# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# openMind is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import argparse
import os
import textwrap

from .cli_utils import safe_load_yaml
from ..pipelines import pipeline
from .subcommand import SubCommand
from ..utils.hub import OPENMIND_CACHE
from ..utils.constants import DYNAMIC_ARG, SPECIFIED_ARGS
from ..models.auto import AutoConfig, AutoTokenizer
from ..utils import get_framework, logging, replace_invalid_characters
from ..utils.hub import OpenMindHub

logger = logging.get_logger()
logging.set_verbosity_info()


class Chat(SubCommand):
    """Holds all the logic for the `openmind-cli chat` subcommand."""

    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self._parser = subparsers.add_parser(
            "chat",
            prog="openmind-cli chat",
            help="Start a multi-turn conversation.",
            description="Start a multi-turn conversation.",
            formatter_class=argparse.RawTextHelpFormatter,
            epilog=textwrap.dedent(
                """\
            examples:
                $ openmind-cli chat Baichuan/Baichuan2_7b_chat_pt
                [USER]>>> hello
                [MODEL]>>> [{"generated_text": "hello"}]
            """
            ),
        )
        self._add_arguments()
        self._parser.set_defaults(func=self._start_chat)

    def _add_arguments(self) -> None:
        """Add arguments to the parser"""
        self._parser.add_argument(
            "--task",
            type=str,
            default=None,
            choices=["text-generation"],
            help="Task name for chat.",
        )
        self._parser.add_argument(
            "--config",
            type=str,
            default=None,
            help="Config model id for chat.",
        )
        self._parser.add_argument(
            "--tokenizer",
            type=str,
            default=None,
            help="Tokenizer model id for chat.",
        )
        self._parser.add_argument(
            "--framework",
            type=str,
            default=None,
            choices=["pt", "ms"],
            help="Framework for chat.",
        )
        self._parser.add_argument(
            "--cache_dir",
            type=str,
            default=None,
            help="Local path for caching models.",
        )
        self._parser.add_argument(
            "--yaml_path",
            type=str,
            default=None,
            help="Local path for loading yaml config file.",
        )

    def _prepare_arguments(self, args: argparse.Namespace) -> dict:
        args_dict = vars(args)
        args_dict.pop("func")

        # assemble arguments according to priority
        if args_dict.get(DYNAMIC_ARG) is None:
            raise ValueError("Repo id is required but not found.")

        if args_dict.get("yaml_path") is not None:
            yaml_content_dict = safe_load_yaml(args_dict.pop("yaml_path"))
            args_dict.update(yaml_content_dict)

        args_dict.update(args_dict.pop(SPECIFIED_ARGS))

        # remove redundant `yaml_path` param if exists
        args_dict.pop("yaml_path", None)

        model_name_or_path = args_dict.pop(DYNAMIC_ARG)

        task = args_dict.pop("task", None)
        if not os.path.exists(model_name_or_path):
            if task is None:
                # infer task name according to repo_id
                task_from_repo = OpenMindHub.get_task_from_repo(model_name_or_path, token=args_dict.get("token", None))
                if task_from_repo is not None:
                    task = task_from_repo
                else:
                    logger.warning(f"Can not infer task name from repo id {model_name_or_path} automatically.")

        # param `--task` is required when using MindSpore model.
        if get_framework() == "ms" and task is None:
            raise ValueError("Param `--task` is required when using MindSpore model for chat, please specify manually.")

        args_dict.update({"task": task, "model": model_name_or_path})

        # set default value
        if args_dict.get("framework") is None:
            args_dict.update({"framework": get_framework()})

        if args_dict.get("cache_dir") is None:
            args_dict.update({"cache_dir": OPENMIND_CACHE})

        if args_dict.get("trust_remote_code") is None:
            logger.info(
                "Param `trust_remote_code` is not specified, default value is `False`, "
                "set to `True` when using files from repo, please make sure remote files are safe."
            )
            args_dict.update({"trust_remote_code": False})

        # initialize config/model/tokenizer if not model id
        if isinstance(args_dict.get("config"), dict):
            args_dict.update({"config": AutoConfig.from_pretrained(**args_dict.get("config"))})

        if isinstance(args_dict.get("tokenizer"), dict):
            args_dict.update({"tokenizer": AutoTokenizer.from_pretrained(**args_dict.get("tokenizer"))})

        return args_dict

    def _start_chat(self, args: argparse.Namespace) -> None:
        args_dict = self._prepare_arguments(args)

        chat_pipeline = pipeline(**args_dict)

        logger.info("Welcome to use openmind chat")

        while True:
            try:
                user_query = input("\n[USER]>>> ")
            except UnicodeDecodeError:
                logger.error(
                    "Decoding error occurred when processing user inputs, please set the terminal encoding " "to utf-8."
                )
                continue
            except Exception as ex:
                err_msg = f"Exception occurred when processing user inputs, detail error message: {str(ex)}"
                raise RuntimeError(replace_invalid_characters(err_msg))

            if user_query.strip() == "exit":
                break

            model_rsp = chat_pipeline(user_query)

            print(f"\n[MODEL]>>> {model_rsp}")
