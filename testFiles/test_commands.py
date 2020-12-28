import os
import subprocess


def scrappie_basecall():
	bcCmd = "scrappie raw " + fastPath + " > " + os.getcwd() + "/Data/basecall/reads.fa"
	subprocess.run([bcCmd], check = True)


def flappie_basecall():
	flappieBcCmd = "flappie " + fastPath + " > " + os.getcwd() + "/Data/basecall/reads.fq"
	subprocess.run([flappieBcCmd], check = True)


def export_scrappie_path():
	expCmd = "export PATH=$PATH:scrappie/build"
    os.system(expCmd)


def scrappie_basecall_single():
	bcCmd = "scrappie raw " + fastPath + "single > " + os.getcwd() + "/Data/basecall/reads.fa"
	os.system(bcCmd)


def flappie_basecall_single():
	flappieBcCmd = "flappie " + fastPath + "single > " + os.getcwd() + "/Data/basecall/reads.fq"
	os.system(flappieBcCmd)
