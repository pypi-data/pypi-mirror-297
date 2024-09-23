# Copyright (c) Huawei Technologies Co., Ltd. 2024, All rights reserved.
# Copyright 2022 The HuggingFace Team. All rights reserved.
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

from dataclasses import dataclass, field
import functools
import os
from typing import Callable, Optional
import warnings

import accelerate
from accelerate.utils import MegatronLMPlugin as AccelerateMegatronLMPlugin


MODEL_CONFIGS_TO_MEGATRON_PARSERS = {}


@dataclass
class MegatronLMPlugin(AccelerateMegatronLMPlugin):
    custom_megatron_datasets_provider_function: Optional[Callable] = field(
        default=None,
        metadata={"help": "Custom megatron train_valid_test datasets provider function."},
    )
    custom_get_batch_function: Optional[Callable] = field(
        default=None,
        metadata={"help": "Custom get batch function."},
    )
    custom_loss_function: Optional[Callable] = field(
        default=None,
        metadata={"help": "Custom loss function."},
    )

    def set_network_size_args(self, model, batch_data=None):
        model_config_type = model.config.model_type.lower()
        for model_type in MODEL_CONFIGS_TO_MEGATRON_PARSERS.keys():
            if model_type in model_config_type:
                MODEL_CONFIGS_TO_MEGATRON_PARSERS[model_type](self, model, batch_data)
                return
        raise ValueError(
            f"Accelerate Megatron-LM integration not supports {model_config_type} model. "
            "You can add your own model config parser."
        )


def add_model_config_to_megatron_parser(model_type: str):
    def add_model_config_parser_helper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        MODEL_CONFIGS_TO_MEGATRON_PARSERS[model_type] = func
        return wrapper

    return add_model_config_parser_helper


@add_model_config_to_megatron_parser("megatron-bert")
def parse_bert_config(megatron_lm_plugin, model, batch_data):
    model_type_name = "bert"
    num_layers = model.config.num_hidden_layers
    hidden_size = model.config.hidden_size
    num_attention_heads = model.config.num_attention_heads
    max_position_embeddings = model.config.max_position_embeddings
    num_labels = model.config.num_labels
    orig_vocab_size = model.config.vocab_size
    if "maskedlm" in model.__class__.__name__.lower():
        pretraining_flag = True
    else:
        raise ValueError("Accelerate Megatron only support maskedlm megatron-bert model.")
    if megatron_lm_plugin.seq_length is not None:
        if megatron_lm_plugin.encoder_seq_length is not None:
            warnings.warn("Both `seq_length` and `encoder_seq_length` are set. Using `encoder_seq_length`.")
        megatron_lm_plugin.seq_length = megatron_lm_plugin.encoder_seq_length
    elif megatron_lm_plugin.encoder_seq_length is not None:
        megatron_lm_plugin.seq_length = megatron_lm_plugin.encoder_seq_length
    elif batch_data is not None:
        megatron_lm_plugin.seq_length = batch_data["input_ids"].shape[1]
    else:
        megatron_lm_plugin.seq_length = max_position_embeddings
    megatron_lm_plugin.megatron_lm_default_args["seq_length"] = megatron_lm_plugin.seq_length
    megatron_lm_plugin.megatron_lm_default_args["model_type_name"] = model_type_name
    megatron_lm_plugin.megatron_lm_default_args["num_layers"] = num_layers
    megatron_lm_plugin.megatron_lm_default_args["hidden_size"] = hidden_size
    megatron_lm_plugin.megatron_lm_default_args["num_attention_heads"] = num_attention_heads
    megatron_lm_plugin.megatron_lm_default_args["max_position_embeddings"] = max_position_embeddings
    megatron_lm_plugin.megatron_lm_default_args["pretraining_flag"] = pretraining_flag
    megatron_lm_plugin.megatron_lm_default_args["orig_vocab_size"] = orig_vocab_size
    megatron_lm_plugin.megatron_lm_default_args["model_return_dict"] = model.config.return_dict
    megatron_lm_plugin.megatron_lm_default_args["num_labels"] = num_labels


@add_model_config_to_megatron_parser("gpt2")
def parse_gpt2_config(megatron_lm_plugin, model, batch_data):
    model_type_name = "gpt"
    num_layers = model.config.n_layer
    hidden_size = model.config.n_embd
    num_attention_heads = model.config.n_head
    max_position_embeddings = model.config.n_positions
    orig_vocab_size = model.config.vocab_size
    pretraining_flag = True
    if megatron_lm_plugin.seq_length is not None:
        if megatron_lm_plugin.decoder_seq_length is not None:
            warnings.warn("Both `seq_length` and `decoder_seq_length` are set. Using `decoder_seq_length`.")
        megatron_lm_plugin.seq_length = megatron_lm_plugin.decoder_seq_length
    elif megatron_lm_plugin.decoder_seq_length is not None:
        megatron_lm_plugin.seq_length = megatron_lm_plugin.decoder_seq_length
    elif batch_data is not None:
        megatron_lm_plugin.seq_length = batch_data["input_ids"].shape[1]
    else:
        megatron_lm_plugin.seq_length = max_position_embeddings
    megatron_lm_plugin.megatron_lm_default_args["seq_length"] = megatron_lm_plugin.seq_length
    megatron_lm_plugin.megatron_lm_default_args["return_logits"] = megatron_lm_plugin.return_logits
    megatron_lm_plugin.megatron_lm_default_args["tokenizer_type"] = "GPT2BPETokenizer"
    megatron_lm_plugin.megatron_lm_default_args["model_type_name"] = model_type_name
    megatron_lm_plugin.megatron_lm_default_args["num_layers"] = num_layers
    megatron_lm_plugin.megatron_lm_default_args["hidden_size"] = hidden_size
    megatron_lm_plugin.megatron_lm_default_args["num_attention_heads"] = num_attention_heads
    megatron_lm_plugin.megatron_lm_default_args["max_position_embeddings"] = max_position_embeddings
    megatron_lm_plugin.megatron_lm_default_args["pretraining_flag"] = pretraining_flag
    megatron_lm_plugin.megatron_lm_default_args["orig_vocab_size"] = orig_vocab_size
    megatron_lm_plugin.megatron_lm_default_args["model_return_dict"] = model.config.return_dict


@add_model_config_to_megatron_parser("t5")
def parse_t5_config(megatron_lm_plugin, model, batch_data):
    model_type_name = "t5"
    num_layers = model.config.num_layers
    hidden_size = model.config.d_model
    num_attention_heads = model.config.num_heads
    max_position_embeddings = model.config.n_positions if hasattr(model.config, "n_positions") else 1024
    orig_vocab_size = model.config.vocab_size
    pretraining_flag = True
    if megatron_lm_plugin.encoder_seq_length is None:
        if batch_data is not None:
            megatron_lm_plugin.encoder_seq_length = batch_data["input_ids"].shape[1]
        else:
            megatron_lm_plugin.encoder_seq_length = max_position_embeddings
    if megatron_lm_plugin.decoder_seq_length is None:
        if batch_data is not None:
            megatron_lm_plugin.decoder_seq_length = batch_data["labels"].shape[1]
        else:
            megatron_lm_plugin.decoder_seq_length = max_position_embeddings
    megatron_lm_plugin.megatron_lm_default_args["encoder_seq_length"] = megatron_lm_plugin.encoder_seq_length
    megatron_lm_plugin.megatron_lm_default_args["decoder_seq_length"] = megatron_lm_plugin.decoder_seq_length
    megatron_lm_plugin.megatron_lm_default_args["model_type_name"] = model_type_name
    megatron_lm_plugin.megatron_lm_default_args["num_layers"] = num_layers
    megatron_lm_plugin.megatron_lm_default_args["hidden_size"] = hidden_size
    megatron_lm_plugin.megatron_lm_default_args["num_attention_heads"] = num_attention_heads
    megatron_lm_plugin.megatron_lm_default_args["max_position_embeddings"] = max_position_embeddings
    megatron_lm_plugin.megatron_lm_default_args["pretraining_flag"] = pretraining_flag
    megatron_lm_plugin.megatron_lm_default_args["orig_vocab_size"] = orig_vocab_size
    megatron_lm_plugin.megatron_lm_default_args["model_return_dict"] = model.config.return_dict


@add_model_config_to_megatron_parser("llama")
def parse_llama_config(megatron_lm_plugin, model, batch_data):
    model_type_name = "gpt"
    num_layers = model.config.num_hidden_layers
    pretraining_flag = True
    hidden_size = model.config.hidden_size
    num_attention_heads = model.config.num_attention_heads
    orig_vocab_size = model.config.vocab_size

    max_position_embeddings = getattr(model.config, "max_position_embeddings")
    seq_length = getattr(model.config, "max_sequence_length", None)
    if megatron_lm_plugin.seq_length is None:
        if seq_length is not None:
            megatron_lm_plugin.seq_length = seq_length
        elif megatron_lm_plugin.decoder_seq_length is not None:
            megatron_lm_plugin.seq_length = megatron_lm_plugin.decoder_seq_length
        elif batch_data is not None:
            megatron_lm_plugin.seq_length = batch_data["input_ids"].shape[1]
        else:
            megatron_lm_plugin.seq_length = max_position_embeddings

    megatron_lm_plugin.megatron_lm_default_args["return_logits"] = megatron_lm_plugin.return_logits
    megatron_lm_plugin.megatron_lm_default_args["tokenizer_type"] = "Llama2Tokenizer"
    megatron_lm_plugin.megatron_lm_default_args["model_type_name"] = model_type_name
    megatron_lm_plugin.megatron_lm_default_args["num_layers"] = num_layers
    megatron_lm_plugin.megatron_lm_default_args["pretraining_flag"] = pretraining_flag
    megatron_lm_plugin.megatron_lm_default_args["hidden_size"] = hidden_size
    megatron_lm_plugin.megatron_lm_default_args["num_attention_heads"] = num_attention_heads
    megatron_lm_plugin.megatron_lm_default_args["orig_vocab_size"] = orig_vocab_size
    megatron_lm_plugin.megatron_lm_default_args["max_position_embeddings"] = max_position_embeddings
    megatron_lm_plugin.megatron_lm_default_args["seq_length"] = megatron_lm_plugin.seq_length
    megatron_lm_plugin.megatron_lm_default_args["model_return_dict"] = model.config.return_dict


def apply_accelerate_dataclasses_plugin():
    print("*" * 15 + f"PID:{os.getpid()} Applying the accelerate dataclasses plugin." + "*" * 15)
    accelerate.utils.MegatronLMPlugin = MegatronLMPlugin
    accelerate.accelerator.MegatronLMPlugin = MegatronLMPlugin

    accelerate.utils.add_model_config_to_megatron_parser = add_model_config_to_megatron_parser
