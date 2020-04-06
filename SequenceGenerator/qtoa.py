import os, sys


def convertFastq(directory):
    #make fasta directory 
    dircmd = "mkdir " + directory + "fasta"
    os.system(dircmd)
    #get directory of fastq files
    files = os.listdir(directory)
    for file in files:
        fastxcmd = "fastq_to_fasta -i " + directory + str(file) + " -o " + directory + "fasta/" + str(file)[:-1] + "a"
        os.system(fastxcmd)
 
    newFiles = os.listdir(directory)
    for file in newFiles:
        print(file)

