import h5py
import SequenceGenerator.align as align
import os

#test to check if required files are created
def file_test(bed_file, ref_file, sam_file):
    if bed_file == None:
        print("bed file test failed")
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
            print("basecall test failed")
            raise FileNotFoundError

        sam_file = align.minimapAligner(fastfile, ref_file, minDir=(os.getcwd() + "/minimap2"))


    elif ref_file == None and sam_file == None:
        print("ref file test failed")
        raise FileNotFoundError

    elif sam_file == None:
        print("sam file test failed")
        raise FileNotFoundError

    if bed_file != None:
        print("\nbed file test passed")
    if sam_file != None:
        print("sam file test passed")

    return bed_file, ref_file, sam_file


def id_file_test():
    for f in os.listdir("./Data/"):
        if f == "Fast5_ids.txt":
            print("id test passed")
            return


def event_check(filename):
    hdf = h5py.File(filename, 'r')
    fast_keys = hdf.keys()
    if "/Analyses/Basecall_1D_001/BaseCalled_template/Events/" in fast_keys:
        print("events test passed \n")
        show_penguin()

    else:
        #create events(nanopolish code goes here)
        pass


def show_penguin():
    penguin = """
    =============================================================

      **-..L```|
       \        |
        *        \        |```| |```` |\  | |```| |   | ``|`` |\  |
        |     |    \      |___| |___  | \ | |___  |   |   |   | \ |
       /*\    |     \     |     |     |  \| |   | | | |   |   |  \|
      |***\   |      |    |     |____ |   | |___|  \|/   _|_  |   |
      \****\   \     |                              |
       \***/    \   /                               |
        \*/        /
         /___/_____\

    =============================================================

    """
    print(penguin)


def sequence_check():
    pass
