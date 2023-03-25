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


import statistics

from implem.poll import poll_alternatives


def parse_hibou_output(outwrap):
    #
    verdict = None
    length = None
    node_count = None
    elapsed_time = None
    #
    for line in outwrap:
        if "verdict" in line:
            if "WeakPass" in line:
                verdict = "WeakPass"
            elif "Pass" in line:
                verdict = "Pass"
            elif "WeakFail" in line:
                verdict = "WeakFail"
            elif "Fail" in line:
                verdict = "Fail"
            elif "Inconc" in line:
                verdict = "Inconc"
            else:
                print(line)
                raise Exception("some other verdict ?")
        # ***
        if "of length" in line:
            length = int(line.split(" ")[-1].strip()[1:-1])
        # ***
        if "node count" in line:
            node_count = int(line.split(" ")[-1].strip())
        # ***
        if "elapsed" in line:
            elapsed_time = float(line.split(" ")[-1].strip())
        # ***
    #
    mydict = {
        'node_count': node_count,
        'length': length,
        'verdict': verdict,
        'elapsed_time': elapsed_time
    }
    return mydict

def is_sat_via_membership(hsf_file,hif_file,htf_file,crit,num_tries, polling_timeout):
    #
    if crit == "reset":
        hcf_file_wtloc = "crit_reset_wtloc.hcf"
        hcf_file_noloc = "crit_reset_noloc.hcf"
    elif crit == "multiply":
        hcf_file_wtloc = "crit_multiply_wtloc.hcf"
        hcf_file_noloc = "crit_multiply_noloc.hcf"
    #
    command_wtloc = ["./hibou_label.exe", "analyze", hsf_file, hif_file, htf_file, hcf_file_wtloc]
    command_noloc = ["./hibou_label.exe", "analyze", hsf_file, hif_file, htf_file, hcf_file_noloc]
    #
    hibou_result = None
    final_dict = {}
    final_dict['tries_time'] = []
    final_dict['tries_quickest'] = []
    for i in range(0,num_tries):
        (outwrap,id_of_quickest) = poll_alternatives(command_wtloc,command_noloc,0.01, polling_timeout)
        if (outwrap,id_of_quickest) == (None,None):
            return get_on_timeout_result()
        try_dict = parse_hibou_output(outwrap)
        #
        keys = ['length','verdict']
        for key in keys:
            if key in final_dict:
                pass
            else:
                final_dict[key] = try_dict[key]
        #
        final_dict['tries_time'].append(try_dict['elapsed_time'])
        if id_of_quickest == 1:
            final_dict['tries_quickest'].append('WT_LOC')
        elif id_of_quickest == 2:
            final_dict['tries_quickest'].append('NO_LOC')
        elif id_of_quickest == None:
            final_dict['tries_quickest'].append('SAME')
        else:
            raise Exception
        #
    t_total = statistics.median(final_dict['tries_time'])
    final_dict['median_time'] = t_total
    #
    return final_dict


def get_on_timeout_result():
    final_dict = {}
    final_dict['tries_time'] = []
    final_dict['tries_quickest'] = []
    final_dict['length'] = None
    final_dict['verdict'] = 'TIMEOUT'
    final_dict['median_time'] = None
    return final_dict
