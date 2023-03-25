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

import os

from enum import IntEnum

from implem.calls_ana import is_sat_via_membership
from implem.commons import FOLDER_MODEL


class MultiTraceKind(IntEnum):
    ACCEPTED = 1
    SLICE = 2
    SWAP_ACT = 3
    SWAP_COMP = 4
    NOISE = 5

    def kind_repr(self):
        if self == MultiTraceKind.ACCEPTED:
            return "ACPT"
        elif self == MultiTraceKind.SLICE:
            return "SLIC"
        elif self == MultiTraceKind.SWAP_ACT:
            return "SACT"
        elif self == MultiTraceKind.SWAP_COMP:
            return "SCMP"
        elif self == MultiTraceKind.NOISE:
            return "NOIS"


def analysis_process(int_name,crit,num_tries,polling_timeout):
    f = open("{}_{}.csv".format(int_name,crit), "w")
    f.truncate(0)  # empty file
    columns = ["name",
               "kind",
               "verdict",
               "trace_length",
               "hibou_time_tries",
               "hibou_tries_quickest",
               "hibou_time_median"]
    f.write(";".join(columns) + "\n")
    f.flush()
    #
    folders_and_kinds = [("tracegen_{}_explo".format(int_name),MultiTraceKind.ACCEPTED),
                         ("tracegen_{}_slices".format(int_name),MultiTraceKind.SLICE),
                         ("tracegen_{}_noise".format(int_name),MultiTraceKind.NOISE),
                          ("tracegen_{}_swap_act".format(int_name),MultiTraceKind.SWAP_ACT),
                           ("tracegen_{}_swap_comp".format(int_name),MultiTraceKind.SWAP_COMP)]
    #
    hsf_file = os.path.join(FOLDER_MODEL, "{}.hsf".format(int_name))
    hif_file = os.path.join(FOLDER_MODEL, "{}.hif".format(int_name))
    #
    for (folder,kind) in folders_and_kinds:
        print("analyzing {} traces for {}".format(kind.kind_repr(), int_name))
        for htf_file in os.listdir(folder):
            htf_file_name = htf_file[:-4]
            htf_file = os.path.join(folder, htf_file)
            #
            mydict = is_sat_via_membership(hsf_file, hif_file, htf_file, crit, num_tries, polling_timeout)
            f.write("{};{};{};{};{};{};{}\n".format(htf_file_name,
                                                        kind.kind_repr(),
                                                         mydict['verdict'],
                                                         mydict['length'],
                                                         mydict['tries_time'],
                                                         mydict['tries_quickest'],
                                                         mydict['median_time']))
            f.flush()



