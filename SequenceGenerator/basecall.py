import h5py
import subprocess
import os, sys
from ont_fast5_api import fast5_interface
from ont_fast5_api.conversion_tools import multi_to_single_fast5
import h5py

################ The basecall module ################


#need to evaluate if fast5 comes with events/sequence data
def basecall_files(directory):
    #create basecall directory
    dircmd = "mkdir " + os.getcwd() + "/Data/basecall/"
    os.system(dircmd)
    #?walk through directories
    guppy_cmd = "guppy_basecaller -r -i " + directory + " -s " + os.getcwd() + "/Data/basecall/ -c rna_r9.4.1_70bps_hac.cfg"
    #subprocess.Popen("guppy_basecaller")
    os.system(guppy_cmd)


def prepare_files_basecall(directory):
    #go through fast5 files and check if the files is multi or single fast5 file
    #we need a single fast5 file
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".fast5"):
                check_file_type(name)


#check if multi or single fast5
def check_file_type(myfile):
    fobj = fast5_interface.get_fast5_file(os.path.join(root, name))
    if fast5_interface.check_file_type(fobj) == "multi-read":
        #convert file to single fast5
        print("converting fast5 file****")
        multi_to_single_fast5.convert_multi_to_single(os.path.join(root, name), directory, "single")
    


def scrappie_basecall(directory):
    prepare_files_basecall(directory)


