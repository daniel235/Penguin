import os
'''
Working in Data Directory /  All files saved in Data directory
'''

def nanopolish_run(fastDir, basecallDir):
    #call nanopolish command
    #todo change fastq to reads.fastq
    print("basecall dir ", basecallDir)
    for file in os.listdir(basecallDir):
        if file.endswith(".fastq"):
            myCmd = "mv " + basecallDir + file + " " + basecallDir + "reads.fastq"
            os.system(myCmd)

    index_cmd = "nanopolish index -d " + fastDir + " " + basecallDir + "reads.fastq"
    #move into data folder to save files
    os.system("cd Data")
    os.system(index_cmd)
    os.system("cd ..")


def nanopolish_create_ids(fastDir, basecallDir):
    #check if files exist if not run nanopolish
    for file in os.listdir(os.getcwd()):
        if file == "reads.fa.index.readdb":
            return "reads.fa.index.readdb"

        if file == "reads.fasta.index.readdb":
            return "reads.fasta.index.readdb"


    nanopolish_run(fastDir, basecallDir)
    return "reads.fasta.index.readdb"


def nanopolish_create_fasta(fastDir, basecallDir):
    #check if files exist if not run nanopolish
    for file in os.listdir(os.getcwd()):
        if file == "reads.fasta":
            return "reads.fasta"

    nanopolish_run(fastDir, basecallDir)
    return "reads.fasta"


def nanopolish_events(fastDir, basecallDir, referenceFile="Data/"):
    nanopolish_run(fastDir, "Data/basecall/")
    #create aligned sam file and convert to bam file
    #check for fasta
    fasta = "Data/" + nanopolish_create_fasta(fastDir, basecallDir)
    #align to reference
    ref_cmd = "minimap2 -ax map-ont -t 8 " + referenceFile + " " + fasta
    os.system(ref_cmd)
    #remove the .ref
    sam_cmd = "samtools sort -o reads-ref.sorted.bam -T reads.tmp"
    os.system(sam_cmd)
    sam_cmd = "samtools index reads-ref.sorted.bam"
    os.system(sam_cmd)
    #check if bamfile is complete
    bamcheck = "samtools quickcheck reads-ref.sorted.bam"
    os.system(bamcheck)

    #align nanopore events to reference genome
    event_cmd = "nanopolish eventalign --reads reads.fasta --bam reads-ref.sorted.bam --genome " + referenceFile + "--samples --scale-events > reads-ref.eventalign.txt"
    os.system(event_cmd)
    #return events file
    return "reads-ref.eventalign.txt"
