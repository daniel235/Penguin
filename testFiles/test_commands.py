import os
import subprocess


def scrappie_basecall(fastPath):
	bcCmd = "scrappie raw " + fastPath + " > " + os.getcwd() + "/Data/basecall/reads.fa"
	print(bcCmd)
	subprocess.run([bcCmd], check = True)
	#os.system(bcCmd)


def flappie_basecall(fastPath):
	flCmd = "flappie --model r941_rna002 --reverse --delta 1.0 " + fastPath + "/ > /Data/basecall/flappie-basecalls.fq"
	subprocess.run([flappieBcCmd], check = True)
	#os.system(flappieBcCmd)s


def export_scrappie_path():
	expCmd = "export PATH=$PATH:" + os.getcwd() + "scrappie/build"
	os.system(expCmd)


def scrappie_basecall_single(fastPath):
	bcCmd = "scrappie raw " + fastPath + "single > " + os.getcwd() + "/Data/basecall/reads.fa"
	return os.system(bcCmd)
	


def flappie_basecall_single(fastPath):
	flCmd = "flappie --model r941_rna002 --reverse --delta 1.0 " + fastPath + "/single/ > /Data/basecall/flappie-basecalls.fq"
	os.system(flCmd)

	
