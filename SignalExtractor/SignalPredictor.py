import os
import h5py
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import svm
import Models.PrepareData as PD
import SignalExtractor.graph_plots as gp

#iterate through signal events
#figure out how to get accuracy of predictions
#files needed bed file sam file
def get_locations(sam_locs, id):
    locs = []
    print(id)
    #sam format (id:0, chrm num:2, location:3)
    #get sam locations
    #look for id in sam array
    for line in sam_locs:
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


def get_all_modified_locs(bed_locs):
    all_locs = {}
    for line in bed_locs:
        if line[0] in all_locs.keys():
            all_locs[line[0]].append(int(line[1]))

        else:
            all_locs[line[0]] = [int(line[1])]

    return all_locs

def get_modified_locs(bed_locs, id):
    all_locs = {}
    #chrm/loc/fastfileLoc/read_id
    for line in bed_locs:
        if id == line[3]:
            #add location to chromosome
            if line[0] in all_locs.keys():
                all_locs[line[0]].append(int(line[1]))

            else:
                all_locs[line[0]] = [int(line[1])]

    return all_locs


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


def get_bed_data(bed):
    modified_data = []
    with open("./Data/pstrand_chr_modification_coors.txt", 'r') as f:
        for line in f:
            tab_line = line.split( )
            modified_data.append(tab_line)

    return modified_data


def predict(model, fastPath=None, bedFile=None, samFile=None, Idfile=None):
    #stats keeper
    total_pseudo = 0
    total_control = 0
    accuracy = 0
    tKmers = 0

    #stat data structures
    runs = []
    accuracies = []

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
    bed_array = get_bed_data(bedFile)

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
                mod_locs = get_modified_locs(bed_array, ID)
                begin_location, end_location = locs[0][1], locs[0][1] + len(locs[0][2])
                currentPosition = begin_location
                chromosome = locs[0][0]
                #check if fast5 contains pseudouridine
                if ID in modified_ids:
                    correct_guess = 1
                    validationCheck = True
                    print("in a modified fast5")

                else:
                    #control
                    validationCheck = False
                    correct_guess = 0

                #separate kmers with corresponding signals
                kmers, signals = segmentSignal(events, signals)
                #create encoder
                hot_kmers = PD.createEncoder(kmers)

                #pass to model
                for i in range(len(kmers)):
                    if len(kmers[i]) != 0:
                        #as you move along kmers add 1 to current position
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
                            #predicted control
                            if guess < 0.50:
                                if validation((chromosome, currentPosition + 2), mod_locs) == 0:
                                    accuracy += 1

                                print("chromosome ", chromosome, " position ", currentPosition + 2, " ", kmers[i], " control \n")
                                total_control += 1
                            #predicted pseudo
                            else:
                                #check if location is actually modified
                                if validation((chromosome, currentPosition + 2), mod_locs) == 1:
                                    accuracy += 1

                                print("chromosome ", chromosome, " position ", currentPosition + 2, " ", kmers[i], " pseudo \n")
                                total_pseudo += 1

                            print("current accuracy ", accuracy / tKmers)

                            #get stats here
                            if tKmers % 10000 == 0:
                                runs.append(tKmers)
                                accuracies.append(accuracy / tKmers)

    print("finished running Pseudo: ", total_pseudo, " control: ", total_control, " accuracy ", accuracy / tKmers)
    #save plot 
    plt.plot(runs, accuracies)
    plt.xlabel('runs')
    plt.ylabel('accuracy')
    plt.show()
    plt.savefig('position_prediction.png')


def nanopolish_predict(model, eventAlign, fastpath, bedPath, samPath, IdFile, oneHot=True, testing=False):
    #read in event align file
    data = pd.read_csv(eventAlign, sep="\t")
    data = PD.scaleData(data)
    print(data)
    #chromosome 
    chromosomes = data["contig"]
    position = data["position"]
    kmers = data["reference_kmer"]
    mean = data["event_level_mean"]
    std_deviation = data["event_stdv"]
    raw_signal = data["samples"]

    #statistics
    accuracy = 0
    tkmerCount = 0
    total_pseudo = 0
    total_control = 0
    accuracies = []
    runs = []
    psuedo_locations = []

    #get modified locations
    bed_array = get_bed_data(bedPath)
    mod_locs = get_all_modified_locs(bed_array)

    #convert kmers
    #hot_kmers = PD.createEncoder(kmers)
    new_hot_kmers = PD.nano_to_onehot(data)

    print("hot kmers ", data["reference_kmer"])
    onehot=pd.get_dummies(data['reference_kmer'], prefix='reference_kmer')
    hot_kmers = onehot.to_numpy()
    print("hot ", hot_kmers)

    count = 0
    if testing == False:
        for kmer in hot_kmers:
            data.iloc[count]["reference_kmer"] = kmer
            count += 1
            print(count)
    else:
        data.iloc[0]["reference_kmer"] = hot_kmers[0]

    

    #check if middle kmer is a T or U
    for i in range(len(kmers)):
        if kmers[i][2] == 'T':
            tkmerCount += 1
            raw = []
            sig = ""
            #convert string signal into actual float signal
            for char in raw_signal[i]:
                if char != ',':
                    sig += char
                else:
                    raw.append(float(sig))
                    sig = ""
            
            raw.append(float(sig))

            #input4Model = PD.createInstance(hot_kmers[i], raw).reshape((1,-1))
            #guess = model.predict(input4Model, batch_size=1, verbose=1)[0]

            #new svm model
            input4Model = PD.createNanoInstance(data.iloc[i], kmers=hot_kmers[i], hot=oneHot)
            input4Model = input4Model.reshape(1, -1)
            print(input4Model)
            guess = model.predict(input4Model)

            #predicted control
            if guess < 0.50:
                print("chromosome ", chromosomes[i], " position ", position[i] + 2, " ", kmers[i], " control \n")
                total_control += 1
                '''
                if validation((chromosomes[i], position[i] + 2), mod_locs) == 0:
                    print("correct control prediction")
                    accuracy += 1
                    total_control += 1
                    #predicted pseudo
                '''
            else:
                #check if location is actually modified
                print("chromosome ", chromosomes[i], " position ", position[i] + 2, " ", kmers[i], " pseudo \n")
                #add predicted locatin to list of possible pseudo locations
                psuedo_locations.append([chromosomes[i], position[i] + 2, kmers[i]])
                total_pseudo += 1
                '''
                if validation((chromosomes[i], position[i] + 2), mod_locs) == 1:
                    accuracy += 1
                    total_pseudo += 1
                    #get stats here
                    if tkmerCount % 10000 == 0:
                        runs.append(tkmerCount)
                        accuracies.append(accuracy / tkmerCount)
                
            print("current accuracy ", accuracy / tkmerCount)
            '''

        if testing:
            break
        
    #read id location kmer
    print("finished running Pseudo: ", total_pseudo, " control: ", total_control, " accuracy ", accuracy / tkmerCount)
    new_possible_locations(psuedo_locations)
    gp.box_plot(total_pseudo, total_control)
    gp.ven_diagram(total_pseudo, total_control, tkmerCount)


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


def pseudoRatio(pcount, count):
    print("ratio of pseudo:control ->", pcount/count, ":1")


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


def validation(location, bed_locations):
    #read in mod locations
    if location[0] in bed_locations.keys():
        #check for locations
        if location[1] in bed_locations[location[0]]:
            #is modified
            return True

    return False


def new_possible_locations(coords):
    #write to file
    #chromosome/location/kmer/readID
    with open("new_locations.tsv", 'w') as f:
        for coord in coords:
            line = coord[0] + "\t" + coord[1] + "\t" +  coord[2] + "\t" + coord[3]
            f.write(line)
            