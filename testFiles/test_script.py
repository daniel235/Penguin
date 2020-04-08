import h5py

#test to check if required files are created
def file_test(bed_file, ref_file, sam_file):
    if bed_file == None:
        print("bed file missing")
        raise FileNotFoundError

    elif ref_file == None and sam_file == None:
        print("ref file missing")
        raise FileNotFoundError

    elif sam_file == None:
        print("sam file missing")
        raise FileNotFoundError

    return


def id_file_test():
    pass


def event_check(filename):
    hdf = h5py.File(filename, 'r')
    print(hdf.keys())


def sequence_check():
    pass
