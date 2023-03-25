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
import os

from implem.commons import FOLDER_MODEL

def generate_accepted(int_name):
    hsf_file = os.path.join(FOLDER_MODEL, "{}.hsf".format(int_name))
    hif_file = os.path.join(FOLDER_MODEL, "{}.hif".format(int_name))
    hcf_file = os.path.join(FOLDER_MODEL, "{}_explo.hcf".format(int_name))
    #
    hibou_proc = subprocess.Popen(["./hibou_label.exe", "explore", hsf_file, hif_file, hcf_file],
                                  stdout=subprocess.PIPE)
    hibou_proc.wait()
    for line in hibou_proc.stdout:
        print( line )
    outwrap = io.TextIOWrapper(hibou_proc.stdout, encoding="utf-8")
    print(outwrap)
    #

def generate_slices(int_name,accepted_htf_name,num_slices,is_slice_wide):
    #
    hsf_file = os.path.join(FOLDER_MODEL, "{}.hsf".format(int_name))
    tracegen_path = "tracegen_{}_explo".format(int_name)
    acc_htf_file = os.path.join(tracegen_path, "{}.htf".format(accepted_htf_name))
    #
    parent_folder = "tracegen_{}_slices".format(int_name)
    #
    slices_names_prefix = accepted_htf_name.split("_")[-1]
    #
    command = ["./hibou_label.exe", "slice", hsf_file, acc_htf_file, "-p", parent_folder, "-k", "slice", "-n", slices_names_prefix]
    #
    if num_slices != None:
        command += ["-r", str(num_slices)]
        if is_slice_wide:
            command += ["-w"]
    #
    hibou_proc = subprocess.Popen(command,stdout=subprocess.PIPE)
    hibou_proc.wait()
    outwrap = io.TextIOWrapper(hibou_proc.stdout, encoding="utf-8")
    #

def generate_noise_mutant(int_name,slice_htf_name):
    #
    hsf_file = os.path.join(FOLDER_MODEL, "{}.hsf".format(int_name))
    slices_tracegen_path = "tracegen_{}_slices".format(int_name)
    slice_htf_file = os.path.join(slices_tracegen_path, "{}.htf".format(slice_htf_name))
    #
    parent_folder = "tracegen_{}_noise".format(int_name)
    #
    name = "{}_noise".format(slice_htf_name)
    command = ["./hibou_label.exe", "mutate_insert_noise", hsf_file, slice_htf_file, "-p", parent_folder, "-e", "-n", name]
    #
    hibou_proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    hibou_proc.wait()
    outwrap = io.TextIOWrapper(hibou_proc.stdout, encoding="utf-8")
    #

def generate_swap_act_mutant(int_name, slice_htf_name):
    #
    hsf_file = os.path.join(FOLDER_MODEL, "{}.hsf".format(int_name))
    slices_tracegen_path = "tracegen_{}_slices".format(int_name)
    slice_htf_file = os.path.join(slices_tracegen_path, "{}.htf".format(slice_htf_name))
    #
    parent_folder = "tracegen_{}_swap_act".format(int_name)
    #
    name = "{}_swap_act".format(slice_htf_name)
    command = ["./hibou_label.exe", "mutate_swap_actions", hsf_file, slice_htf_file, "-p", parent_folder, "-n", name]
    #
    hibou_proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    hibou_proc.wait()
    outwrap = io.TextIOWrapper(hibou_proc.stdout, encoding="utf-8")
    #

def generate_swap_comp_mutant(int_name, slice1_htf_name, slice2_htf_name):
    #
    hsf_file = os.path.join(FOLDER_MODEL, "{}.hsf".format(int_name))
    slices_tracegen_path = "tracegen_{}_slices".format(int_name)
    slice1_htf_file = os.path.join(slices_tracegen_path, "{}.htf".format(slice1_htf_name))
    slice2_htf_file = os.path.join(slices_tracegen_path, "{}.htf".format(slice2_htf_name))
    #
    parent_folder = "tracegen_{}_swap_comp".format(int_name)
    #
    name = "{}_swap_comp".format(slice1_htf_name)
    command = ["./hibou_label.exe", "mutate_swap_components", hsf_file, slice1_htf_file, slice2_htf_file, "-p", parent_folder, "-n", name]
    #
    hibou_proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    hibou_proc.wait()
    outwrap = io.TextIOWrapper(hibou_proc.stdout, encoding="utf-8")
    #
