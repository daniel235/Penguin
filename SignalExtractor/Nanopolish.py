import os

def nanopolish_create_ids(fastDir):
    #move into nanopolish directory
    os.system("cd nanopolish")
    #call nanopolish command
    index_cmd = "nanopolish index -d " + fastDir + " reads.fasta"
    os.system(index_cmd)
    os.system("cd ..")
    
