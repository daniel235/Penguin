import os

import h5py

import Models.PrepareData as PD

#iterate through signal events
#figure out how to get accuracy of predictions
#files needed bed file sam file
def get_locations(sam, id):
    locs = []
    print(id)
    #sam format (id:0, chrm num:2, location:3)
    #get sam locations
    #look for id in sam array
    for line in sam:
        #match found
        if id == line[0]:
            #get chromosome
            chm = line[1]
            #get chromosome number
            loc = int(line[2])
            #get location in chromosome
            seq = line[4]
            print('added to locs')
            locs.append([chm, loc, seq])

    return locs


def get_sam_data(sam):
    sam_data = []
    #create sam table
    with open(sam, 'r') as f:
        for line in f:
            column = line.split( )
            if len(column) > 0:
                if '@' not in column[0]:
                    #add read id/chromosome number/location/cigar/sequence
                    sam_data.append([column[0], column[2], column[3], column[4], column[9]])

    return sam_data


def predict(model, fastPath=None, bedFile=None, samFile=None, Idfile=None):
    #stats keeper
    total_pseudo = 0
    total_control = 0
    accuracy = 0
    tKmers = 0
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

    #get sam data
    sam_array = get_sam_data(samFile)

    currentLocation = 0

    #read in fast5 files
    #parse data
    for dirpath, subdir, files in os.walk(fastPath):
        for fname in files:
            #read only if fast5 file
            if fname.endswith(".fast5"):
                #get locations here
                fname = fastPath + fname
                #get events and signals from fast5 file
                events, signals, ID = parser(fname)
                #get locations of fast5 file
                locs = get_locations(sam_array, ID)
                begin_location, end_location = locs[0][1], locs[0][1] + len(locs[0][2])
                currentPosition = begin_location
                chromosome = locs[0][0]
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
                        currentPosition += 1
                        if chr(kmers[i][2]) == 'T':
                            tKmers += 1
                            #if signal length is greater than 1
                            if len(signals[i][0]) > 1:
                                signals[i] = list(map(int, signals[i][0]))
                            #if signal length is 1
                            else:
                                signals[i][0] = int(signals[i][0][0])

                            input4Model = PD.createInstance(hot_kmers[i], signals[i]).reshape((1,-1))
                            #probability
                            guess = model.predict(input4Model, batch_size=1, verbose=1)[0]
                            print("guess ", guess)
                            #control
                            if guess < 0.50:
                                if correct_guess == 0:
                                    accuracy += 1

                                print("chromosome ", chromosome, " position ", currentPosition + 2, " ", kmers[i], " control \n")
                                total_control += 1
                            #pseudo
                            else:
                                if correct_guess == 1:
                                    accuracy += 1

                                print(kmers[i], " pseudo \n")
                                total_pseudo += 1

    print("finished running Pseudo: ", total_pseudo, " control: ", total_control, " accuracy ", accuracy / tKmers)


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
        fast5_p_id=hf5.get('Raw/Reads/')
        sas=''.join(list(fast5_p_id.keys()))

        fast5_ids=hf5.get('Raw/Reads/'+sas+'/')
        fast5_ids=fast5_ids.attrs['read_id']

        read_id=fast5_ids.decode('utf-8')


    return events, raw_signal, read_id



def stats(pseudo, control):
    with open("./Data/stats.txt", 'w+') as f:
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
