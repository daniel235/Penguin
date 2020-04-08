import argparse
import os, sys, platform
import SequenceGenerator.sequence as sequence
import Fast5_indexing as indexing
import testFiles.test_script as tscript
import SignalExtractor as Extract
import Models as model

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
tscript.file_test(bedPath, refPath, samPath)
#create ids for files
indexing.Id_parser.parse_fast5_ids(fast5Path=fastPath)

#extract fast5 files with modified coordinates(sam, bed, fast5)
indexing.coord_extract.extract_modified_coords(bedPath, samPath)

#get signals from modified  (???)
coordFile = "./Data/pstrand_chr_modification_coors.txt"
Extract.ModifiedSignal.extract_signal(fastPath, coordFile)


#get file of signals and pass to model
modified = "./Data/post_pseudo_signals_1mer.txt"
control = "./Data/control_signals.txt"

model.NeuralNet.run_neural_net(control, modified)

