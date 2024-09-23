# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""InternLM models' APIs."""
from mindspore import nn

from mindformers.version_control import get_lazy_inline
from mindformers.models import LlamaModel, LlamaForCausalLM
from mindformers.models.utils import set_layer_stage_recompute
from mindformers.tools.register.register import MindFormerModuleType, MindFormerRegister

from .transformer_internlm import InternLMDecodeLayer
from .configuration_internlm import InternLMConfig


cell_reuse = get_lazy_inline


class InternLMModel(LlamaModel):
    """Transformer decoder consisting of *config.num_hidden_layers* layers. Each layer is a [`InternLMDecoderLayer`].

    Args:
        config(InternLMConfig): The config of network.

    """

    config_class = InternLMConfig

    def __init__(self, config: InternLMConfig):
        super().__init__(config)
        self.layers = nn.CellList()
        for layer_id in range(config.num_layers):
            layer = InternLMDecodeLayer(
                batch_size=config.batch_size,
                seq_length=config.seq_length,
                layer_id=layer_id,
                dim=config.hidden_size,
                n_heads=config.num_heads,
                n_kv_heads=config.n_kv_heads,
                intermediate_size=config.intermediate_size,
                multiple_of=config.multiple_of,
                ffn_dim_multiplier=config.ffn_dim_multiplier,
                norm_eps=config.rms_norm_eps,
                compute_dtype=config.compute_dtype,
                layernorm_compute_dtype=config.layernorm_compute_type,
                softmax_compute_dtype=config.softmax_compute_type,
                rotary_dtype=config.rotary_dtype,
                param_init_type=config.param_init_type,
                has_bias=config.has_bias,
                use_past=config.use_past,
                use_flash_attention=config.use_flash_attention,
                use_paged_attention=config.use_paged_attention,
                block_size=config.block_size,
                num_blocks=config.num_blocks,
                is_dynamic=config.is_dynamic,
                use_kvcache_op=config.use_kvcache_op,
                is_flexible_shape=config.is_flexible_shape,
                use_rope_slice=config.use_rope_slice,
                parallel_config=config.parallel_config,
            )
            set_layer_stage_recompute(layer, layer_id, config.offset, config.parallel_config, config.num_layers)
            self.layers.append(layer)


@MindFormerRegister.register(MindFormerModuleType.MODELS)
class InternLMForCausalLM(LlamaForCausalLM):
    """Provide InternLM training loss or logits through network, inherited from [`LlamaForCausalLM`].

    Args:
        config(InternLMConfig): The config of network.

    """

    config_class = InternLMConfig

    @cell_reuse
    def __init__(self, config: InternLMConfig):
        checkpoint_name_or_path = config.checkpoint_name_or_path
        config.checkpoint_name_or_path = ""
        super().__init__(config)
        self.model = InternLMModel(config=config)
        config.checkpoint_name_or_path = checkpoint_name_or_path
        self.load_checkpoint(config)
