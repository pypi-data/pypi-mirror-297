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

import os

from accelerate import Accelerator
from accelerate.utils import (
    MegatronEngine,
    MegatronLMDummyDataLoader,
    MegatronLMDummyScheduler,
    MegatronLMOptimizerWrapper,
    MegatronLMSchedulerWrapper,
    megatron_lm_initialize,
    megatron_lm_prepare_data_loader,
)
import torch
from torch.optim.lr_scheduler import LRScheduler

from .megatron_lm import prepare_model_optimizer_scheduler as megatron_lm_prepare_model_optimizer_scheduler


def _prepare_megatron_lm(self, *args):
    megatron_lm_plugin = self.state.megatron_lm_plugin
    set_megatron_lm_plugin_args(self, megatron_lm_plugin, args)

    # initialize megatron-lm
    megatron_lm_initialize(self, args_defaults=megatron_lm_plugin.megatron_lm_default_args)

    (model, optimizer, scheduler) = megatron_lm_prepare_model_optimizer_scheduler(self)
    self.wait_for_everyone()

    counter = 0
    result = []
    for obj in args:
        if isinstance(obj, torch.utils.data.DataLoader):
            result.append(megatron_lm_prepare_data_loader(self, obj))
            counter += 1
        elif isinstance(obj, MegatronLMDummyDataLoader):
            if counter == 0:
                obj.set_megatron_data_args()
                dataloaders = megatron_lm_prepare_data_loader(self, obj)
            result.append(dataloaders[counter])
            counter += 1
        else:
            result.append(obj)

    if model is not None:
        model = MegatronEngine(self, model, optimizer, scheduler)
    if optimizer is not None:
        optimizer = MegatronLMOptimizerWrapper(optimizer)
    if scheduler is not None:
        scheduler = MegatronLMSchedulerWrapper(scheduler, optimizer)

    for i in range(len(result)):
        if isinstance(result[i], torch.nn.Module):
            result[i] = model
        elif isinstance(result[i], torch.optim.Optimizer):
            result[i] = optimizer
        elif isinstance(result[i], MegatronLMDummyScheduler):
            result[i] = scheduler

    if model is not None:
        self._models.append(model)
        if len(self._models) > 1:
            raise AssertionError(
                "You can't use same `Accelerator()` instance with multiple models when using Megatron-LM"
            )
    if optimizer is not None:
        self._optimizers.append(optimizer)
    if scheduler is not None:
        self._schedulers.append(scheduler)

    return tuple(result)


def set_megatron_lm_plugin_args(self, megatron_lm_plugin, args):
    micro_batch_size = None
    if not megatron_lm_plugin.megatron_dataset_flag:
        batch_sizes = [obj.batch_size for obj in args if hasattr(obj, "batch_size")]
        if len(batch_sizes) == 0:
            raise ValueError(
                "You must specify a training or evaluation dataloader in `accelerate.prepare()` when using Megatron-LM."
            )

        micro_batch_size = min(batch_sizes) if megatron_lm_plugin.is_train_batch_min else max(batch_sizes)
        if len(batch_sizes) > 1:
            print(
                "Since you passed both train and evaluation dataloader, `is_train_batch_min` will decide the "
                "`train_batch_size`. "
            )
    else:
        for obj in args:
            if isinstance(obj, MegatronLMDummyDataLoader):
                micro_batch_size = obj.dataset_args["micro_batch_size"]
                break
    if micro_batch_size is not None:
        dp_degree = self.num_processes // (megatron_lm_plugin.tp_degree * megatron_lm_plugin.pp_degree)
        megatron_lm_plugin.set_training_args(micro_batch_size, dp_degree)
    else:
        print(
            "WARNING: When you do not pass the dataloader parameter, the `data_parallel_size`, "
            "`micro_batch_size`, and `global_batch_size` megatron parameters will not be updated."
        )
    model = None
    optimizer = None
    scheduler = None
    batch_data = None
    for obj in args:
        if isinstance(obj, torch.utils.data.DataLoader) and batch_data is None:
            batch_data = next(iter(obj))
        elif isinstance(obj, torch.nn.Module):
            model = obj
        elif isinstance(obj, (torch.optim.Optimizer)):
            optimizer = obj
        elif isinstance(obj, (LRScheduler, MegatronLMDummyScheduler)):
            scheduler = obj
    if model is not None:
        megatron_lm_plugin.set_network_size_args(model, batch_data)
    if optimizer is not None:
        megatron_lm_plugin.set_optimizer_type(optimizer)
    if scheduler is not None:
        if not isinstance(scheduler, MegatronLMDummyScheduler):
            raise ValueError(
                "You can't use a custom scheduler with Megatron-LM. "
                "Please use the `accelerate.utils.MegatronLMDummyScheduler` instead."
            )
        megatron_lm_plugin.set_scheduler_args(scheduler)


def apply_accelerate_accelerator_plugin():
    print("*" * 15 + f"PID:{os.getpid()} Applying the accelerate megatron plugin." + "*" * 15)
    Accelerator._prepare_megatron_lm = _prepare_megatron_lm
