import h5py
from ont_fast5_api.conversion_tools import multi_to_single_fast5
from ont_fast5_api import fast5_interface
import SequenceGenerator.align as align
import SignalExtractor.Nanopolish as events
from testFiles.test_commands import *
import os, sys
import subprocess



#todo get basecall data
def basecall_test(fastPath):
    #check if basecall file already exists
    files = os.listdir("Data/basecall")
    
    for f in files:
        if f.endswith(".fasta") or f.endswith(".fa") or f.endswith(".fastq") or f.endswith(".fq"):
            if os.stat("Data/basecall/" + f).st_size > 1000:
                return

    print("missing basecall file****/creating basecall file")
    #scrappie cmd
    bcCmd = "scrappie raw " + fastPath + " > " + os.getcwd() + "/Data/basecall/reads.fa"

    #flappie cmd 
    flCmd = "flappie --model r941_rna002 --reverse --delta 1.0 " + fastPath + "/ > /Data/basecall/flappie-basecalls.fq"
    #create basecall file 
    try:
        #todo 26ts
        #output = subprocess.run([bcCmd], check = True)
        output = subprocess.run([flCmd], check=True)
        #scrappie_basecall(fastPath)

    #checking if file not in right fast5 format(multi/single)
    except subprocess.CalledProcessError:
        #export_scrappie_path()
        print("got error / process error")
        
        #checking if already in single directory
        if 'single' in fastPath:
            print("|||\/|| Already in single folder")

        #todo insert flappie
        #convert multi fast5 to single fast5 and move files into single directory.  
        elif 'single' not in os.listdir(fastPath):
            print("converting fast5 to single fast5")
            convert_fast5_type(fastPath)
            #scrappie_basecall_single(fastPath)
            flappie_basecall_single(fastPath)

    #if path doesn't exist or no files
    except FileNotFoundError:
        #export_scrappie_path()
        print("got error / no file found ")
        #output = scrappie_basecall_single(fastPath)
        try:
            output = flappie_basecall_single(fastPath)
        except:
            if 'single' not in os.listdir(fastPath):
                convert_fast5_type(fastPath)
                #scrappie_basecall_single(fastPath)

            flappie_basecall_single(fastPath)


        sys.exit()
    
    '''
    #any error (default error"export scrappie and try again")
    except:
        export_scrappie_path()
        scrappie_basecall(fastPath)
    '''
    #check if basecall created successfully
    if os.stat("Data/basecall/reads.fa").st_size > 0:
        print("created basecall file ****")
    elif os.stat("Data/basecall/flappie-basecalls.fq").st_size > 0:
        print("created fastq basecall ****")
    else:
        print("Couldn't create basecall file")

    

#test to check if required files are created
def file_test(bed_file, ref_file, sam_file):
    if bed_file == None:
        print("bed file test failed****")
        raise FileNotFoundError
    
    #set ref file 
    if ref_file != None:
        #fasta input
        fastfile = os.getcwd() + "/Data/basecall/"
        for ffile in os.listdir(fastfile):
            if ffile.endswith(".fastq") or ffile.endswith(".fasta") or ffile.endswith(".fa"):
                #check if fasta files exist in directory
                fastfile = os.getcwd() + "/Data/basecall/" + ffile

        #check if you found a fasta/fastq file in directory
        if fastfile.endswith(".fastq") != True and fastfile.endswith(".fasta") != True and fastfile.endswith(".fa") != True:
            print("basecall test failed****")
            raise FileNotFoundError


    #download reference file
    else:
        #use default ref files
        refFlag = False
        #defaultReferenceFile = "Homo_sapiens.GRCh38.dna.alt.fa"
        #defaultReferenceFile = "refgenome"
        defaultReferenceFile = "grch38.fna"
        #defaultReferenceFile = "coli-ref.fa"
        downloadedFlag = False
        #check if default reference file exists
        for f in os.listdir(os.getcwd()):
            if f == defaultReferenceFile:
                print("reference downloaded already****")
                downloadedFlag = True
        #download reference file
        if downloadedFlag != True:
            #os.system("wget -O refgenome.tar.gz ftp://igenome:G3nom3s4u@ussd-ftp.illumina.com/Homo_sapiens/Ensembl/GRCh37/Homo_sapiens_Ensembl_GRCh37.tar.gz")
            #os.system("wget -O refgenome.gz ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh37_latest/refseq_identifiers/GRCh37_latest_genomic.fna.gz")
            os.system("wget -O grch38.fna.gz ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/GCA_000001405.15_GRCh38_genomic.fna.gz")
            #os.system("wget -O ftp://ftp.ensembl.org/pub/release-100/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.alt.fa.gz")
            #os.system("tar -xzf refgenome.tar.gz")
            #os.system("gunzip refgenome.gz")
            os.system("gzip -d grch38.fna.gz")
            print("gunzipping reference genome****")
            #os.system("gunzip -v Homo_sapiens.GRCh38.dna.alt.fa.gz")
            for f in os.listdir(os.getcwd()):
                if f == "Homo_sapiens" or f == defaultReferenceFile or f == "refgenome":
                    refFlag = True
                    break
        
        ref_file = defaultReferenceFile
        #if file download wasn't successful
        if refFlag == False and downloadedFlag != True:
            print("ref file test failed****")
            raise FileNotFoundError

        #get basecalled file
        fastfile = os.getcwd() + "/Data/basecall/"
        for ffile in os.listdir(fastfile):
            if ffile.endswith(".fastq") or ffile.endswith(".fasta") or ffile.endswith(".fa"):
                #check if fast files exist in directory
                fastfile += ffile
                break

        #if no fasta/fastq file found
        if fastfile == os.getcwd() + "/Data/basecall/":
            print("basecall file test failed****")
            raise FileNotFoundError
        
        
    if sam_file == None:
        #ref file exists so align here
        sam_file = get_sam_file(fastfile, ref_file)

    elif sam_file == None:
        print("sam file test failed****")
        raise FileNotFoundError

    if bed_file != None:
        print("\nbed file test passed****")
    if sam_file != None:
        print("sam file test passed****")

    return bed_file, ref_file, sam_file


def id_file_test():
    for f in os.listdir("./Data/"):
        if f == "Fast5_ids.txt":
            print("id test passed****")
            return

def get_sam_file(fastfile, ref_file):
    #check if sam file exists on our directory
    if "Alignment.sam" in os.listdir("Data"):
        #prompt to create new sam file
        choice = input("Do you want to create a new sam file?(y/n)")
        if choice == 'y':
            sam_file = align.minimapAligner(fastfile, ref_file)
        else:
            return "Data/Alignment.sam"

    else:
        sam_file = align.minimapAligner(fastfile, ref_file)

    return sam_file

#create event info file for machine learning models
def event_check(fpath=None, filename=None, ref=None, NanopolishOnly=True):
    #check if event info already exists
    if "reads-ref.eventalign.txt" in os.listdir("Data") and os.stat("Data/reads-ref.eventalign.txt").st_size > 1000:
            return "Data/reads-ref.eventalign.txt"

    #no events
    if ref != None:
        #todo fix this bug
        if event_align_check() == None:
            print("Creating Event Align file****")
            #create events(nanopolish code goes here)
            #is it a single file or path
            if fpath == None:
                event_file = events.nanopolish_events(filename, "Data/basecall/", referenceFile=ref)
            else:
                event_file = events.nanopolish_events(fpath, "Data/basecall/", referenceFile=ref)
                
            print("event file ", event_file)
            show_penguin()
            return event_file
        else:
            show_penguin()
            return "Data/reads-ref.eventalign.txt"
    else:
        print("reference file test failed")
        raise FileNotFoundError



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


def event_align_check():
    for file in os.listdir("Data"):
        if file == "reads-ref.eventalign.txt" and os.stat("Data/reads-ref.eventalign.txt").st_size > 1000:
            print("Event Align Test Passed****")
            return "Data/reads-ref.eventalign.txt"


    print("Event Align Test Failed****")
    return None


def convert_fast5_type(directory):
    #go through fast5 files and check if the files is multi or single fast5 file
    #we need a single fast5 file
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".fast5"):
                fobj = fast5_interface.get_fast5_file(os.path.join(root, name))
                if fast5_interface.check_file_type(fobj) == "multi-read":
                    #convert file to single fast5
                    print("converting fast5 " + name + " file****" )
                    multi_to_single_fast5.convert_multi_to_single(os.path.join(root, name), directory, "single")
 
