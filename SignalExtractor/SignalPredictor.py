import os

import h5py

import Models.PrepareData as PD

#iterate through signal events
#figure out how to get accuracy of predictions
#files needed bed file sam file


def predict(model, fastPath=None, bedFile=None, samFile=None, Idfile=None):
    #read in fast5 files
    #parse data
    events, signals = parser(fastPath)
    kmers, signals = segmentSignal(events, signals)

    #create encoder
    hot_kmers = PD.createEncoder(kmers)

    #pass to model
    for kmer, signal in hot_kmers, signals:
        input4Model = PD.createInstance(kmer, signal)
        guess = model.predict(input4Model)
    
        if guess == 0:
            print(kmer, " control \n")
        else:
            print(kmer, " pseudo \n")


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


def parser(fastPath):
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
                #get events
                events = hf5.get('/Analyses/Basecall_1D_001/BaseCalled_template/Events/')
                events = events.value

    return raw_signal, events


def stats():
    pass


def segmentSignal(events, signal):
    lengths = []
    kmers = []
    signal_instances = []
    kmer = ""
    signalLen = 0
    for i, row in enumerate(events):
        #next signal
        if row[5] != 0:
            lengths.append(signalLen)
            signalLen = 0
            kmers.append(kmer)

        else:
            #add event length
            signalLen += row[3]

        kmer = row[0]

    #cut up signal
    current = 0
    for size in lengths:
        signal_instances.append([signal[current:current+size+1]])
        current += size + 1

    return kmers, signal_instances

#visualize
def show_window():
    #pygame?
    pass
