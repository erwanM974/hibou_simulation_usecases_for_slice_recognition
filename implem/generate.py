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

import random

from implem.commons import try_mkdir,empty_directory
from implem.calls_gen import *


def reset_directories(int_name):
    folders = ["tracegen_{}_explo".format(int_name),
               "tracegen_{}_slices".format(int_name),
               "tracegen_{}_noise".format(int_name),
               "tracegen_{}_swap_act".format(int_name),
               "tracegen_{}_swap_comp".format(int_name)]
    #
    for parent_folder in folders:
        try_mkdir(parent_folder)
        empty_directory(parent_folder)


def generation_process(int_name,num_slices_per_mu,is_slice_wide):
    #
    reset_directories(int_name)
    #
    print("exploring semantics for " + int_name)
    generate_accepted(int_name)
    #
    print("generating slices for " + int_name)
    tracegen_path = "./tracegen_{}_explo".format(int_name)
    for acc_htf_file_name in os.listdir(tracegen_path):
        acc_htf_file_name = acc_htf_file_name[:-4]
        generate_slices(int_name,acc_htf_file_name,num_slices_per_mu,is_slice_wide)
    #
    print("generating mutants for " + int_name)
    slicegen_path = "./tracegen_{}_slices".format(int_name)
    all_slices_names = [slice_htf_file_name[:-4] for slice_htf_file_name in os.listdir(slicegen_path)]
    for i in range(0,len(all_slices_names)):
        slice_htf_file_name = all_slices_names[i]
        #
        generate_noise_mutant(int_name,slice_htf_file_name)
        generate_swap_act_mutant(int_name,slice_htf_file_name)
        #
        other_to_swap_with = None
        while ((other_to_swap_with == None) or (other_to_swap_with == slice_htf_file_name)):
            other_to_swap_with = random.choice(all_slices_names)
        #
        generate_swap_comp_mutant(int_name,slice_htf_file_name,other_to_swap_with)

