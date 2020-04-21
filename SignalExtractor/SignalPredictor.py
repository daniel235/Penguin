import os

import h5py

import Models.PrepareData as PD

#iterate through signal events
#figure out how to get accuracy of predictions
#files needed bed file sam file
def get_locations():
    pass



def predict(model, fastPath=None, bedFile=None, samFile=None, Idfile=None):
    #stats keeper
    total_pseudo = 0
    total_control = 0
    accuracy = 0
    #set up locations of modifications
    if bedFile != None:
        #start process for getting id's and mod coords
        #load modified locations ids
        modified_ids = []
        with open("./Data/pstrand_chr_modification_coors.txt", 'r') as f:
            for line in f:
                tab_line = line.split( )
                modified_ids.append(tab_line[3])

    else:
        print("No validation just prediction")


    currentLocation = 0

    #read in fast5 files
    #parse data
    for dirpath, subdir, files in os.walk(fastPath):
        for fname in files:
            #read only if fast5 file
            if fname.endswith(".fast5"):
                fname = fastPath + fname
                #get events and signals from fast5 file
                events, signals, ID = parser(fname)
                #check if fast5 contains pseudouridine
                if ID in modified_ids:
                    correct_guess = 1
                    print("in a modified fast5")

                else:
                    #control
                    correct_guess = 0

                #separate kmers with corresponding signals
                kmers, signals = segmentSignal(events, signals)
                #create encoder
                hot_kmers = PD.createEncoder(kmers)

                #pass to model
                for i in range(len(kmers)):
                    if len(kmers[i]) != 0:
                        if chr(kmers[i][2]) == 'T':
                            if len(signals[i][0]) > 1:
                                signals[i] = list(map(int, signals[i][0]))
                            else:
                                signals[i][0] = int(signals[i][0][0])

                            input4Model = PD.createInstance(hot_kmers[i], signals[i]).reshape((1,-1))
                            #probability
                            guess = model.predict(input4Model, batch_size=1, verbose=1)[0]
                            print("guess ", guess)
                            if guess < 0.50:
                                if correct_guess == 1:
                                    accuracy += 1

                                print(kmers[i], " control \n")
                                total_control += 1
                            else:
                                if correct_guess == 0:
                                    accuracy += 1

                                print(kmers[i], " pseudo \n")
                                total_pseudo += 1

    print("finished running Pseudo: ", total_pseudo, " control: ", total_control, " accuracy ", accuracy / len(kmers))


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

        #get id
        fast5_p_id=h5f.get('Raw/Reads/')
        sas=''.join(list(fast5_p_id.keys()))

        fast5_ids=h5f.get('Raw/Reads/'+sas+'/')
        fast5_ids=fast5_ids.attrs['read_id']

        read_id_v=fast5_ids.decode('utf-8')


    return events, raw_signal, read_id


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






def validation(location, bed_locations):
    #read in bed file
    pass
