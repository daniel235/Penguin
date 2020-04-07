import argparse
import os, sys, platform
import SequenceGenerator.sequence as sequence

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
sequence.prep_required_files(bedFile, fast5Path=directory, referenceFile=refFile, samFile=samFile)



