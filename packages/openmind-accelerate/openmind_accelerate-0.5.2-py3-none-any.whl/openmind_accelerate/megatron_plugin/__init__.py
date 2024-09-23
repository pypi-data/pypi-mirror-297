# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# openMind Accelerate is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import importlib.util

if importlib.util.find_spec("megatron") is None or importlib.util.find_spec("megatron.data") is None:
    raise EnvironmentError("You must use '--no-use-pep517' to pip install nvidia's megatron from source.")

from .imports import apply_accelerate_imports_plugin

apply_accelerate_imports_plugin()

from .dataclasses import apply_accelerate_dataclasses_plugin

apply_accelerate_dataclasses_plugin()

from .megatron_lm import apply_accelerate_megatron_lm_plugin

apply_accelerate_megatron_lm_plugin()

from .accelerator import apply_accelerate_accelerator_plugin

apply_accelerate_accelerator_plugin()
