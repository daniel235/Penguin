import os

import h5py

import Models.PrepareData as PD

#iterate through signal events
#figure out how to get accuracy of predictions
#files needed bed file sam file


def predict(model, fastPath=None, bedFile=None, samFile=None, Idfile=None):
    #stats keeper
    total_pseudo = 0
    total_control = 0
    #read in fast5 files
    #parse data
    for dirpath, subdir, files in os.walk(fastPath):
        for fname in files:
            if fname.endswith(".fast5"):
                fname = fastPath + fname
                events, signals = parser(fname)
                
                kmers, signals = segmentSignal(events, signals)
                #print("kmers ", kmers)
                #create encoder
                hot_kmers = PD.createEncoder(kmers)

                #pass to model
                for i in range(len(kmers)):
                    if len(kmers[i]) != 0:
                        #if kmers[i][2] == 'T':
                        #todo fix inputs
                        print("sigs ", signals[i])
                        input4Model = PD.createInstance(hot_kmers[i], signals[i])
                        guess = model.predict(input4Model)
                        print(input4Model)
                        if guess == 0:
                            print(kmers[i], " control \n")
                            total_control += 1
                        else:
                            print(kmers[i], " pseudo \n")
                            total_pseudo += 1

    print("finished running Pseudo: ", total_pseudo, " control: ", total_control)


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


def parser(fastfile):
    if fastfile.endswith(".fast5"):
        #add full path
        hf5 = h5py.File(fastfile, 'r')
        #todo just extract signal and pass it to model
        #extract signal  
        raw_data=list(hf5['/Raw/Reads/'].values())[0]
        raw_signal=raw_data['Signal'].value
        #get events
        events = hf5.get('/Analyses/Basecall_1D_001/BaseCalled_template/Events/')
        events = events.value

    return events, raw_signal


def stats(pseudo, control):
    with open("./Data/stats.py", 'w+') as f:
        l1 = "pseudo count " + pseudo
        l2 = "not pseudo count " + control
        f.write(l1)
        f.write(l2)


def segmentSignal(events, signal):
    lengths = []
    kmers = []
    signal_instances = []
    kmer = ""
    signalLen = 0
    for i, row in enumerate(events):
        #move to next signal
        #print("row ", row)
        if int(row[5]) != 0:
            lengths.append(signalLen)
            signalLen = 0
            kmers.append(kmer)

        else:
            #add event length
            signalLen += int(row[3])

        kmer = row[4]

    #cut up signal
    current = 0
    for size in lengths:
        signal_instances.append([signal[current:current+size+1]])
        current += size + 1

    return kmers, signal_instances

'''
#visualize
def show_window():
    #pygame?
    pass
'''

def stats():
    pass