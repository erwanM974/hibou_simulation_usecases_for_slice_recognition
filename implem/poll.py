#
# Copyright 2023 Erwan Mahe (github.com/erwanM974)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import subprocess
import io
import time


def poll_alternatives(command1,command2,refresh_rate,polling_timeout):
    #
    proc1 = subprocess.Popen(command1, stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(command2, stdout=subprocess.PIPE)
    #
    cumul_time = 0
    while cumul_time < polling_timeout:
        #
        if proc1.poll() != None:
            outwrap = io.TextIOWrapper(proc1.stdout, encoding="utf-8")
            if proc2.poll() != None:
                return (outwrap,None)
            else:
                proc2.kill()
                return (outwrap,1)
        elif proc2.poll() != None:
            proc1.kill()
            outwrap = io.TextIOWrapper(proc2.stdout, encoding="utf-8")
            return (outwrap, 2)
        else:
            cumul_time += refresh_rate
            time.sleep( refresh_rate )
    #
    proc1.kill()
    proc2.kill()
    return (None,None)

