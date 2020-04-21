import h5py
import SequenceGenerator.align as align
import os

#test to check if required files are created
def file_test(bed_file, ref_file, sam_file):
    if bed_file == None:
        print("bed file missing")
        raise FileNotFoundError

    #create aligned sam
    elif ref_file != None and sam_file == None:
        #fasta input
        fastfile = os.getcwd() + "/Data/basecall/"
        for ffile in os.listdir(fastfile):
            if ffile.endswith(".fastq") or ffile.endswith(".fasta"):
                #check if fast files exist in directory 
                fastfile = os.getcwd() + "/Data/basecall/" + ffile

        if fastfile.endswith(".fastq") != True and fastfile.endswith(".fasta") != True:
            raise FileNotFoundError

        sam_file = align.minimapAligner(fastfile, ref_file, minDir=(os.getcwd() + "/minimap2"))


    elif ref_file == None and sam_file == None:
        print("ref file missing")
        raise FileNotFoundError

    elif sam_file == None:
        print("sam file missing")
        raise FileNotFoundError

    return bed_file, ref_file, sam_file


def id_file_test():
    pass


def event_check(filename):
    hdf = h5py.File(filename, 'r')
    print(hdf.keys())


def sequence_check():
    pass
