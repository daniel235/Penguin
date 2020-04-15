
import sys, getopt
import h5py, numpy as np, os, sys
import itertools

# import matplotlib.pyplot as plt
import SignalExtractor.eventHelper as eH
from SignalExtractor.eventHelper import f_events


def extract_control(IdPath, modCoordFile):
    inp = modCoordFile
    inp2 = IdPath

    #id
    id_dict=dict()
    file=open(inp2,'r')
    for i in file:
        i1=i.split( )
        # print(i1[2])
        id_dict[i1[2]] = [i1[0]]
        id_dict[i1[2]].append(i1[1])
        id_dict[i1[2]].append(i1[3])
        id_dict[i1[2]].append(i1[2])

    cnt=0

    with open("./Data/control_signals.txt", 'w+') as f:
        f_dict=dict()
        #coord
        file2=open(inp,'r')
        for q in file2:
            q1=q.split( )
            if q1[3] in id_dict:
                #path / filename
                f_name=id_dict[q1[3]][0]+' '+id_dict[q1[3]][1]
                if f_name in f_dict:
                    f_dict[f_name].append(int(q1[2]))
                    
                else:
                    f_dict[f_name] = [int(q1[2])]
        #key filename / coord fast 5 positions
        for keys, values in f_dict.items():
                p=keys.split(' ')
                r=p[0]+'/'+p[1]

                hdf = h5py.File(r,'r')

                #### Extract signal
                try:
                    raw_data=list(hdf['/Raw/Reads/'].values())[0]
                    raw_signal=raw_data['Signal'].value
                    ### Extract events
                    events_data=hdf.get('/Analyses/Basecall_1D_001/BaseCalled_template/Events/')

                    events=events_data.value
                    ### Extract start time
                    start_time=hdf.get('Raw/Reads/')
                    sas=''.join(list(start_time.keys()))

                    start_t=hdf.get('Raw/Reads/'+sas+'/')
                    start_t=start_t.attrs['start_time']
                    ### Extract duration
                    Du_time=hdf.get('Raw/Reads/'+sas+'/')
                    Du_time=Du_time.attrs['duration']
                    ### Extract Fastq
                    Fastq_data=hdf.get('/Analyses/Basecall_1D_001/BaseCalled_template/Fastq/')
                    summary_data=hdf.get('/Analyses/Basecall_1D_000/Summary/basecall_1d_template/')
                    c_freq = hdf.get('/UniqueGlobalKey/context_tags/')
                    c_freq = (c_freq.attrs['sample_frequency']).decode('utf-8')
                    raw_fastq=(Fastq_data.value).decode('utf-8')
                    fastq_decoded=raw_fastq.split('\n')
                except AttributeError:
                    # print('skipped')
                    continue           
            # #################### Shifted to helper function module ################################
                len_seq=len(''.join(fastq_decoded[1]))
                a_seq_nos=[]
                for ase in values:
                    a_seq_no=(len_seq-int(ase))+1
                    a_seq_nos.append(int(a_seq_no))

                final_eves=eH.event_scrapper(events)
                seq_no=3

                for e, i in enumerate(final_eves):
                    seq_no=seq_no+int(i[1])
                    len_seq=len(''.join(fastq_decoded[1]))
                    a_seq_no=(len_seq-int(q1[2]))+1
                ##### Tail pass
                    if e > 2 and e < len(final_eves)-2 and i[0][2:][:1] == 'A':
                        if seq_no not in a_seq_nos:
                            f_e=f_events(final_eves,e)
                            if len(f_e) != 0:
                                start=[]
                                end=[]
                                for s in f_e:
                                    for t in range(5):
                                        start.append(s[t][2])
                                        end.append(s[t][4])
                                          
                                min_st=min(start)
                                max_stl=(max(end)-min(start))+1
                                sig='_'.join(map(str, raw_signal[min_st:][:max_stl]))
                                # print(p[1]+' '+i[0]+' '+str(min_st)+'_'+str(max_stl)+' '+sig)
                                f.write(p[1]+' '+i[0]+' '+str(min_st)+'_'+str(max_stl)+' '+sig+'\n')
                                cnt=cnt+1
                                print("Number of control signals extracted: "+str(cnt))
