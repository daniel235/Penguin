import h5py
import os
#iterate through signal events
#figure out how to get accuracy of predictions
#files needed bed file sam file


def predict(model, fastPath=None, bedFile=None, samFile=None, Idfile=None):
    id_dict = createIdParser(Idfile)
    #read in fast5 files
    for dirpath, subdir, files in os.walk(fastPath):
        for fname in files:
            if fname.endswith(".fast5"):
                hf5 = h5py.File(fname, 'r')
                #todo just extract signal and pass it to model
                #extract signal 
                raw_data=list(hf5['/Raw/Reads/'].values())[0]
                raw_signal=raw_data['Signal'].value
                #pass to model
                guess = model.evaluate(raw_signal)


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
