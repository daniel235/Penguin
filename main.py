import argparse
import os, sys, platform
from keras.models import Sequential
import SequenceGenerator.sequence as sequence
import Fast5_indexing.coord_extract as coord
import Fast5_indexing.Id_parser as Id
import testFiles.test_script as tscript
import SignalExtractor.ModifiedSignal as Extract
import SignalExtractor.UnmodifiedSignal as ExtractControl
import SignalExtractor.SignalPredictor as Predict
#import Models.NeuralNet as model
import Models.PrepareData as PD
import Models.RunModels as RM
from SequenceGenerator import input_object

#check for all files
parser = argparse.ArgumentParser(description="Start of Getting Nanopore Signals")

#input folder of fast5 files
parser.add_argument('-i', action='store', dest='path_input', help='Provide Fast5 folder path')
#bed file argument
parser.add_argument('-b', action='store', dest='bed_input', help='Provide Bed file')
#reference genome to align (If missing events must provide reference file)
parser.add_argument('-ref', action='store', dest='ref_input', help='Provide reference genome file')
#sam file
parser.add_argument('-s', action='store', dest='sam_input', help='Provide Sam File')
#testing
parser.add_argument('-test', action='store', dest='test_input', help='Testing')

#docker run
#environment variables
path_input = os.getenv("MY_FAST5_PATH")
bed_input = os.getenv("MY_BED_FILE")
ref_input = os.getenv("MY_REFERENCE_GENOME")
sam_input = os.getenv("MY_SAM_FILE")
test_input = os.getenv("IS_A_TEST")

#get arguments
results = parser.parse_args()
#directory argument
directory = results.path_input
bedFile = results.bed_input
refFile = results.ref_input
samFile = results.sam_input
testingInput = results.test_input

#create input object
my_input_object = input_object.InputObject(directory)

############### Prepare all files needed ###################################
#check if files are basecalled
tscript.basecall_test(directory)
#get all required files for signal extraction
bedPath, fastPath, refPath, samPath = sequence.prep_required_files(bedFile, fast5Path=directory, referenceFile=refFile, samFile=samFile)
#test if files are all available
bedPath, refPath, samPath = tscript.file_test(bedPath, refPath, samPath)

############################################################################

print("---bed path ", bedPath)
print("---reference path ", refPath)
print("---sam path ", samPath)


############### Get directory or single file and check for events ##########

#singular file
if fastPath.endswith(".fast5"):
    currentFile = fastPath
    event_info = tscript.event_check(filename=currentFile, ref=refPath)
#path of fast5 files
else:
    for root, dirs, files in os.walk(fastPath, topdown=False):
        for name in files:
            if name.endswith(".fast5"):
                currentFile = name
                break

    event_info = tscript.event_check(fpath=fastPath, filename=currentFile, ref=refPath)

#############################################################################



############### Parse out necessary data for extraction #####################

#create ids for files
Id.parse_fast5_ids(fast5Path=fastPath)

#extract fast5 files with modified coordinates(sam, bed, fast5)
coord.extract_modified_coords(bedPath, samPath)

#get signals from modified  (???) (hardcoded)
coordFile = "./Data/pstrand_chr_modification_coors.txt"
Idfile = "./Data/Fast5_ids.txt"

#Extract.extract_signal(Idfile, coordFile)
#ExtractControl.extract_control(Idfile, coordFile)

#get file of signals and pass to model
modified = "./Data/post_pseudo_signals.txt"
control = "./Data/control_signals.txt"

##############################################################################



################# Get correct machine learning network #######################

#model.run_neural_net(control, modified)
#PD.createInstance(control, modified)

#load model
model = PD.prepareNNModel()

'''
#already has event information
if event_info == None:
    Predict.predict(model, fastPath=fp, bedFile=bedPath, samFile=samPath)
    #RM.run_nn(model, [])
'''
#added events from nanopolish

#model = PD.prepareSVMModel("Models/modelsvmHot.joblib")
#model = PD.prepareSVMModel("Models/svm")
model = PD.prepareNNModel()
Predict.nanopolish_predict(model, event_info, fastPath, bedPath, samPath, Idfile, testing=False)

################################################################################