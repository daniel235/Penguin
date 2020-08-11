import h5py
from ont_fast5_api.conversion_tools import multi_to_single_fast5
from ont_fast5_api import fast5_interface
import SequenceGenerator.align as align
import SignalExtractor.Nanopolish as events
import os

#todo get basecall data
def basecall_test(fastPath):
    files = os.listdir("Data/basecall")
    for f in files:
        if f.endswith(".fasta") or f.endswith(".fa") or f.endswith(".fastq"):
            return

    print("missing basecall file****")
    print("creating basecall file****")
    #create basecall file
    bcCmd = "scrappie raw " + fastPath + " > " + os.getcwd() + "/Data/basecall/scrappieReads.fa"
    try:
        os.system(bcCmd)
    except:
        print("got error")
    print("created basecall file****")


#test to check if required files are created
def file_test(bed_file, ref_file, sam_file):
    if bed_file == None:
        print("bed file test failed****")
        raise FileNotFoundError
    
    #check for basecall keys


    #create aligned sam
    elif ref_file != None and sam_file == None:
        #fasta input
        fastfile = os.getcwd() + "/Data/basecall/"
        for ffile in os.listdir(fastfile):
            if ffile.endswith(".fastq") or ffile.endswith(".fasta"):
                #check if fast files exist in directory
                fastfile = os.getcwd() + "/Data/basecall/" + ffile

        if fastfile.endswith(".fastq") != True and fastfile.endswith(".fasta") != True:
            print("basecall test failed****")
            raise FileNotFoundError

        sam_file = align.minimapAligner(fastfile, ref_file)


    elif ref_file == None and sam_file == None:
        #use default ref files
        refFlag = False
        #defaultReferenceFile = "Homo_sapiens.GRCh38.dna.alt.fa"
        defaultReferenceFile = "refgenome"
        downloadedFlag = False
        #check if default reference file exists
        for f in os.listdir(os.getcwd()):
            if f == defaultReferenceFile:
                print("reference downloaded already****")
                downloadedFlag = True

        if downloadedFlag != True:
            print("RECOMMENDED to download first")
            print("WARNING: default reference file is 18gb in size, ..downloading")
            #os.system("wget -O refgenome.tar.gz ftp://igenome:G3nom3s4u@ussd-ftp.illumina.com/Homo_sapiens/Ensembl/GRCh37/Homo_sapiens_Ensembl_GRCh37.tar.gz")
            os.system("wget -O refgenome.gz ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh37_latest/refseq_identifiers/GRCh37_latest_genomic.fna.gz")
            #os.system("wget -O ftp://ftp.ensembl.org/pub/release-100/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.alt.fa.gz")
            os.system("tar -xzf refgenome.tar.gz")
            os.system("gunzip refgenome.gz")
            print("gunzipping reference genome****")
            #os.system("gunzip -v Homo_sapiens.GRCh38.dna.alt.fa.gz")
            for f in os.listdir(os.getcwd()):
                print(f)
                if f == "Homo_sapiens" or f == defaultReferenceFile or f == "refgenome":
                    refFlag = True
                    break

        ref_file = defaultReferenceFile

        if refFlag == False and downloadedFlag != True:
            print("ref file test failed****")
            raise FileNotFoundError

        #get basecalled file
        fastfile = os.getcwd() + "/Data/basecall/"
        for ffile in os.listdir(fastfile):
            if ffile.endswith(".fastq") or ffile.endswith(".fasta"):
                #check if fast files exist in directory
                fastfile += ffile
                break
        
        if fastfile == os.getcwd() + "/Data/basecall/":
            print("basecall file test failed****")
            raise FileNotFoundError

        #ref file exists so align here
        sam_file = align.minimapAligner(fastfile, ref_file)

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


def event_check(fpath=None, filename=None, ref=None, NanopolishOnly=True):
    #single file
    if fpath == None:
        hdf = h5py.File(filename, 'r')
        #check if event file exists
        if "reads-ref.eventalign.txt" in os.listdir("Data"):
            return "Data/reads-ref.eventalign.txt"

    #multiple files
    else:
        hdf = h5py.File(fpath + filename, 'r')

    fast_keys = hdf.keys()
    if "/Analyses/Basecall_1D_001/BaseCalled_template/Events/" in fast_keys and not NanopolishOnly:
        print("events test passed**** \n")
        show_penguin()
        return None
    #no events
    else:
        if ref != None:
            if event_align_check() == None:
                print("Creating Event Align file****")
                #create events(nanopolish code goes here)
                event_file = events.nanopolish_events(fpath, "Data/basecall/", ref)
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
        if file == "reads-ref.eventalign.txt":
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
                    multi_to_single_fast5.

                

    fast5_interface.check_file_type()
