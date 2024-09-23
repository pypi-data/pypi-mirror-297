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
import warnings


ASCEND_HOME_PATH = os.environ.get("ASCEND_HOME_PATH", None)
if ASCEND_HOME_PATH:
    print("*" * 15 + f"PID:{os.getpid()} It's an NPU environment, start using the megatron and npu plugins." + "*" * 15)
    from . import npu_plugin

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from . import megatron_plugin
else:
    print("*" * 15 + f"PID:{os.getpid()} It's not an NPU environment, start using the megatron plugin." + "*" * 15)
    from . import megatron_plugin
