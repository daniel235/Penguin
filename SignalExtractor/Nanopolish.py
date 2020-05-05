import os
'''
Working in Data Directory /  All files saved in Data directory
'''

def nanopolish_run(fastDir, basecallDir):
    #call nanopolish command
    #todo change fastq to reads.fastq
    index_cmd = "nanopolish index -d " + fastDir + " -s " + basecallDir + " sequencing_summary.txt reads.fastq"
    #move into data folder to save files
    os.system("cd Data")
    os.system(index_cmd)
    os.system("cd ..")


def nanopolish_create_ids(fastDir):
    #check if files exist if not run nanopolish
    for file in os.listdir(os.getcwd()):
        if file == "reads.fa.index.readdb":
            return "reads.fa.index.readdb"

        if file == "reads.fasta.index.readdb":
            return "reads.fasta.index.readdb"


    nanopolish_run(fastDir)
    return "reads.fasta.index.readdb"


def nanopolish_create_fasta(fastDir):
    #check if files exist if not run nanopolish
    for file in os.listdir(os.getcwd()):
        if file == "reads.fasta":
            return "reads.fasta"

    nanopolish_run(fastDir)
    return "reads.fasta"


def nanopolish_events(fastDir, referenceFile="Data/"):
    nanopolish_run(fastDir, "Data/basecall/")
    #create aligned sam file and convert to bam file
    #check for fasta
    fasta = "Data/" + nanopolish_create_fasta(fastDir)
    #align to reference
    ref_cmd = "minimap2 -ax map-ont "+ referenceFile + " " + fasta  " > mySam.sam"
    os.system(ref_cmd)
    #remove the .ref
    sam_cmd = "samtools sort -o reads-" + referenceFile[:-3] + ".sorted.bam -T reads.tmp"
    os.system(sam_cmd)
    sam_cmd = "samtools index reads-" + referenceFile[:-3] + ".sorted.bam"
    os.system(sam_cmd)
    #check if bamfile is complete
    bamcheck = "samtools quickcheck reads-" + referenceFile[:-3] + ".sorted.bam"
    os.system(bamcheck)

    #align nanopore events to reference genome
    event_cmd = "nanopolish eventalign --reads reads.fasta --bam reads-" + referenceFile[:-3] + ".sorted.bam --genome " + referenceFile + "--samples --scale-events > reads-" + referenceFile[:-3] + ".eventalign.txt"
    os.system(event_cmd)
    #return events file
    return "reads-" + referenceFile[:-3] + ".eventalign.txt"
