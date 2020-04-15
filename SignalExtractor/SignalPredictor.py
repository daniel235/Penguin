import os

import h5py

import Models.PrepareData as PD

#iterate through signal events
#figure out how to get accuracy of predictions
#files needed bed file sam file


def predict(model, fastPath=None, bedFile=None, samFile=None, Idfile=None):
    #id_dict = createIdParser(Idfile)
    #read in fast5 files
    for dirpath, subdir, files in os.walk(fastPath):
        for fname in files:
            if fname.endswith(".fast5"):
                #add full path
                fname = fastPath + fname
                hf5 = h5py.File(fname, 'r')
                #todo just extract signal and pass it to model
                #extract signal 
                raw_data=list(hf5['/Raw/Reads/'].values())[0]
                raw_signal=raw_data['Signal'].value
                #pass to model
                tempKmer = 'TTTTT'
                input4Model = PD.createInstance(tempKmer, raw_signal)
                guess = model.predict(input4Model)
                #todo parse up signal into kmer signals
                if guess == 0:
                    print(fname + " control \n")
                else:
                    print(fname + " pseudo \n")


def createIdParser(IdFile):
    id_dict=dict()
    with open(IdFile, 'r') as f:
        for i in f:
            i1=i.split( )
            #path/file/id/run
            id_dict[i1[2]] = [i1[0]]
            id_dict[i1[2]].append(i1[1])
            id_dict[i1[2]].append(i1[3])

    return id_dict


def findLocation():
    pass


def stats():
    pass


#visualize
def show_window():
    #pygame?
    pass
