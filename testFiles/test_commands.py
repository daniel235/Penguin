import os
import subprocess


def scrappie_basecall(fastPath):
	bcCmd = "scrappie raw " + fastPath + " > " + os.getcwd() + "/Data/basecall/reads.fa"
	subprocess.run([bcCmd], check = True)


def flappie_basecall(fastPath):
	flappieBcCmd = "flappie " + fastPath + " > " + os.getcwd() + "/Data/basecall/reads.fq"
	subprocess.run([flappieBcCmd], check = True)


def export_scrappie_path():
	expCmd = "export PATH=$PATH:" + os.getcwd() + "scrappie/build"
	os.system(expCmd)


def scrappie_basecall_single(fastPath):
	bcCmd = "scrappie raw " + fastPath + "single > " + os.getcwd() + "/Data/basecall/reads.fa"
	os.system(bcCmd)


def flappie_basecall_single(fastPath):
	flappieBcCmd = "flappie " + fastPath + "single > " + os.getcwd() + "/Data/basecall/reads.fq"
	os.system(flappieBcCmd)
