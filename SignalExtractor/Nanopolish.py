import os
'''
Working in Data Directory /  All files saved in Data directory
'''

def nanopolish_run(fastDir, basecallDir):
    #call nanopolish command
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

def convertToFasta(fastq):
    #name for final file
    fname = ""
    if fastq.endswith(".fq"):
        convCmd = "paste - - - - < " + fastq + " | cut -f 1,2| sed 's/^@/>/' | tr '\t' '\n' > " +  fastq[:-3] + ".fq"
        fname = fastq[:-3] + ".fasta"

    else:
        convCmd = "paste - - - - < " + fastq + " | cut -f 1,2| sed 's/^@/>/' | tr '\t' '\n' > " +  fastq[:-6] + ".fastq"
        fname = fastq[:-6] + ".fasta"

    print("fname ", fname)
    os.system(convCmd)
    

    return fname


def nanopolish_events(fastDir, basecallDir, referenceFile="Data/"):
    nanopolish_run(fastDir, "Data/basecall/")
    #create aligned sam file and convert to bam file
    fasta = "Data/" + nanopolish_create_fasta(fastDir, basecallDir)
    #convert file 
    for file in os.listdir(basecallDir):
        if file.endswith(".fastq") or file.endswith(".fq"):
            fasta = convertToFasta(file)

    #align to reference
    ref_cmd = "minimap2 -ax map-ont -t 8 " + referenceFile + " " + basecallDir + fasta + " | " + "samtools sort -o " + basecallDir + "reads-ref.sorted.bam -T " + basecallDir + "reads.tmp | samtools index " + basecallDir + "reads-ref.sorted.bam"  
    print("current command ", ref_cmd)
    os.system(ref_cmd)
    #remove the .ref
    '''
    sam_cmd = "samtools sort -o reads-ref.sorted.bam -T reads.tmp"
    os.system(sam_cmd)
    sam_cmd = "samtools index reads-ref.sorted.bam"
    os.system(sam_cmd)'''
    #check if bamfile is complete
    bamcheck = "samtools quickcheck reads-ref.sorted.bam"
    os.system(bamcheck)

    #align nanopore events to reference genome
    event_cmd = "nanopolish eventalign --reads reads.fasta --bam reads-ref.sorted.bam --genome " + referenceFile + "--samples --scale-events > reads-ref.eventalign.txt"
    os.system(event_cmd)
    #return events file
    return "reads-ref.eventalign.txt"
