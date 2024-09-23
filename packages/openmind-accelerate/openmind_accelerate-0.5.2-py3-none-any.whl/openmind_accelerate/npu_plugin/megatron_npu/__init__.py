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

import os


print("*" * 15 + f"PID:{os.getpid()} Applying the megatron npu plugin." + "*" * 15)
import torch
import torch_npu
import mindspeed.megatron_adaptor
from torch_npu.contrib import transfer_to_npu
