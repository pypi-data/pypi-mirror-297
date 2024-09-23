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

import functools
import importlib
import importlib.metadata
import importlib.util
import os
import sys
import types


def version_wrapper(fn):
    @functools.wraps(fn)
    def wrapper(distribution_name, *args, **kwargs):
        from packaging.version import Version

        if distribution_name == "megatron-lm":
            return "2.2.0"
        elif distribution_name == "megatron-core":
            original_version = fn(distribution_name, *args, **kwargs)
            if Version(original_version) < Version("0.5.0"):
                return "0.5.0"
            return original_version
        return fn(distribution_name, *args, **kwargs)

    return wrapper


def is_megatron_lm_available():
    from accelerate.utils import str_to_bool

    if str_to_bool(os.environ.get("ACCELERATE_USE_MEGATRON_LM", "False")) == 1:
        if importlib.util.find_spec("megatron") is not None:
            return True
    return False


def apply_accelerate_imports_plugin():
    print("*" * 15 + f"PID:{os.getpid()} Applying the accelerate imports plugin." + "*" * 15)
    old_version_fn = importlib.metadata.version
    importlib.metadata.version = version_wrapper(importlib.metadata.version)

    import megatron
    import megatron.core
    import megatron.core.enums
    import megatron.model

    megatron.model.ModelType = megatron.core.enums.ModelType
    megatron.model.DistributedDataParallel = megatron.core.distributed.DistributedDataParallel
    import megatron.core.pipeline_parallel

    sys.modules["megatron.schedules"] = types.ModuleType("schedules")
    setattr(
        sys.modules["megatron.schedules"],
        "get_forward_backward_func",
        megatron.core.pipeline_parallel.get_forward_backward_func,
    )

    import accelerate

    importlib.reload(accelerate)  # Avoid externally imported accelerate
    importlib.reload(accelerate.utils)
    importlib.reload(accelerate.accelerator)
    importlib.reload(accelerate.utils.megatron_lm)
    accelerate.utils.is_megatron_lm_available = is_megatron_lm_available
    accelerate.accelerator.is_megatron_lm_available = is_megatron_lm_available
    accelerate.utils.megatron_lm.is_megatron_lm_available = is_megatron_lm_available

    importlib.metadata.version = old_version_fn
