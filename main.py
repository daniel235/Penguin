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

#check for all files
parser = argparse.ArgumentParser(description="Start of Getting Nanopore Signals")

#input folder of fast5 files
parser.add_argument('-i', action='store', dest='path_input', help='Provide Fast5 folder path')
#bed file argument
parser.add_argument('-b', action='store', dest='bed_input', help='Provide Bed file')
#reference genome to align
parser.add_argument('-ref', action='store', dest='ref_input', help='Provide reference genome file')
#sam file
parser.add_argument('-s', action='store', dest='sam_input', help='Provide Sam File')
#purpose (Signal Extraction/ Signal Prediction)
parser.add_argument('-e', action='store', dest='use_input', help='Extraction')
#Prediction
parser.add_argument('-p', action='store', dest='pred_input', help='Prediction')


#get arguments
results = parser.parse_args()
#directory argument
directory = results.path_input
bedFile = results.bed_input
refFile = results.ref_input
samFile = results.sam_input

#get all required files for signal extraction
bedPath, fastPath, refPath, samPath = sequence.prep_required_files(bedFile, fast5Path=directory, referenceFile=refFile, samFile=samFile)
#test if files are all available
bedPath, refPath, samPath = tscript.file_test(bedPath, refPath, samPath)

#todo insert nanopolish script(test script takes care of this)
#events test
currentFiles = os.listdir(fastPath)
currentFile = None
for f in currentFiles:
    if f.endswith(".fast5"):
        currentFile = f
        break

tscript.event_check(fastPath + currentFile)

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


#model.run_neural_net(control, modified)
#PD.createInstance(control, modified)

#load model
model = PD.prepareNNModel()
#PD.createInstance()
fp = fastPath
Predict.predict(model, fastPath=fp, bedFile=bedPath)
#RM.run_nn(model, [])
