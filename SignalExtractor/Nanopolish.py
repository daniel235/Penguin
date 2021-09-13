import os
'''
Working in Data Directory /  All files saved in Data directory
'''

def merge_fastq(basecallDir):
    merge_cmd = "cat "
    for file in os.listdir(basecallDir):
        if file.endswith(".fastq"):
            merge_cmd += file + " "
        
    merge = "> " + basecallDir + " reads.fastq"
    merge_cmd += merge
    os.system(merge_cmd)


def nanopolish_run(fastDir, basecallDir):
    #call nanopolish command
    '''
    for file in os.listdir(basecallDir):
        if file.endswith(".fastq"):
            myCmd = "mv " + basecallDir + file + " " + basecallDir + "reads.fastq"
            os.system(myCmd)
    '''
    #create one fastq file
    merge_fastq(basecallDir)
    #convertToFasta("Data/basecall/reads.fastq")
    #todo check for single folder in fastdir directory
    index_cmd = "nanopolish index -d " + fastDir + " " + basecallDir + "reads.fa"
    #move into data folder to save files

    os.system(index_cmd)


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
    #check if file empty
    if "reads.fastq" not in os.listdir(os.getcwd() + "/Data/basecall"):
        print("no reads.fastq")
        #check for scrappie fasta
        print("get ", os.getcwd() + "/Data/basecall")
        if "scrappieReads.fa" in os.listdir(os.getcwd() + "/Data/basecall"):
            print("scrappie provided fasta")
            fname = "scrappieReads.fa"
            #change scrappiereads to reads.fasta
            changeNameCmd = "mv Data/basecall/scrappieReads.fa Data/basecall/reads.fasta"
            os.system(changeNameCmd)

    elif fastq.endswith(".fq"):
        convCmd = "paste - - - - < " + fastq + " | cut -f 1,2| sed 's/^@/>/' | tr '\t' '\n' > " +  fastq[:-3] + ".fa"
        fname = fastq[:-3] + ".fa"
        os.system(convCmd)

    else:
        convCmd = "paste - - - - < " + fastq + " | cut -f 1,2| sed 's/^@/>/' | tr '\t' '\n' > " +  fastq[:-6] + ".fasta"
        fname = fastq[:-6] + ".fasta"
        os.system(convCmd)

    
    return fname


def nanopolish_events(fastDir, basecallDir, referenceFile="Data/", fastFile=None):
    print("in nanopolish events")
    nanopolish_run(fastDir, "Data/basecall/")
    fasta = ""
    #create aligned sam file and convert to bam file
    #check for fasta first in basecall directory
    for files in os.listdir("Data/basecall"):
        if files.endswith(".fa") or files.endswith(".fasta"):
            fasta = "Data/basecall/" + files
            print("found fasta already in directory")
            break

    if fasta == "":
        fasta = "Data/basecall/" + nanopolish_create_fasta(fastDir, basecallDir)

    
    '''
    #convert file
    for file in os.listdir(basecallDir):
        if file.endswith(".fastq") or file.endswith(".fq"):
            fasta = convertToFasta(file)
            fastqCount += 1
    '''
    #align to reference / send to bam file
    #todo hardcode for now
    sam_cmd = "minimap2 -ax map-ont " + referenceFile + " /Data/basecall/flappie-basecalls.fq > Aln.sam"
    os.system(sam_cmd)
    ref_cmd = "minimap2 -ax map-ont " + referenceFile + " /Data/basecall/flappie-basecalls.fq" + " | " + "samtools sort -o " + basecallDir + "reads-ref.sorted.bam -T " + basecallDir + "reads.tmp"
    print("current command ", ref_cmd)
    os.system(ref_cmd)

    #index a genome bam file to extract alignments overlapping particular genomic regions
    sam_cmd = "samtools index " + basecallDir + "reads-ref.sorted.bam"
    os.system(sam_cmd)
    
    #check if bamfile is complete
    bamcheck = "samtools quickcheck " + basecallDir + "reads-ref.sorted.bam"
    os.system(bamcheck)

    #align nanopore events to reference genome
    event_cmd = "nanopolish eventalign --reads " + basecallDir + "reads.fasta --bam " + basecallDir + "reads-ref.sorted.bam --genome " + referenceFile + " --scale-events > Data/reads-ref.eventalign.txt  --samples"
    os.system(event_cmd)
    #return events file
    return "Data/reads-ref.eventalign.txt"
