import h5py
import subprocess
import os, sys


#need to evaluate if fast5 comes with events/sequence data
def basecall_files(directory):
    #create basecall directory
    dircmd = "mkdir " + os.getcwd() + "Data/basecall/"
    os.system(dircmd)
    #?walk through directories
    guppy_cmd = "guppy_basecaller -i " + directory + " -s " + os.getcwd() + "/Data/basecall/ -c rna_r9.4.1_70bps_hac.cfg"
    #subprocess.Popen("guppy_basecaller")
    os.system(guppy_cmd)

