import os, sys

def guppyAligner(inputFile, ref):
    #make align directory
    try:
        dircmd = "mkdir " + inputFile + "sam"
        os.system(dircmd)
    except:
        pass

    alignCmd = "guppy_aligner -i " + inputFile + " -s " + inputFile + "sam/ -a " + ref
    os.system(alignCmd)


def minimapAligner(ifile, ref):
    #go into minimap directory
    alcmd = "./minimap2/minimap2 -ax map-ont " + ref + " " + ifile + " > " + "Data/Alignment.sam"
    os.system(alcmd)
    return "Data/Alignment.sam"


'''
https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.1/bowtie2-2.4.1-linux-x86_64.zip/download


https://dl.bintray.com/boostorg/release/1.72.0/source/boost_1_72_0.tar.bz2

http://ccb.jhu.edu/software/tophat/downloads/test_data.tar.gz

ftp://ftp.ccb.jhu.edu/pub/data/bowtie_indexes/GRCh38_no_alt.zip'''
