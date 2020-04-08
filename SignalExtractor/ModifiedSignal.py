#!/usr/bin/env python

import getopt
import argparse

import sys, getopt

import h5py, numpy as np, os, sys

import itertools

# import matplotlib.pyplot as plt
import SignalExtractor.eventHelper as eH
from SignalExtractor.eventHelper import f_events


# ########################################### file control ########################################
def extract_signal(fast5path, modCoordFile):
    #coord file
    inp = modCoordFile
    #fast5path
    inp2 = fast5path

    print(inp)
    print(inp2)

    id_dict=dict()
    
    with open(inp2, 'r') as f:
        for i in f:
            print(i)
            i1=i.split( )
            print(i1[2])
            id_dict[i1[2]] = [i1[0]]
            id_dict[i1[2]].append(i1[1])
            id_dict[i1[2]].append(i1[3])

    cnt=0

    with open('./Data/post_pseudo_signals_1mer.txt','w') as f:
        file2=open(inp,'r')
        for q in file2:
            q1=q.split( )
            if q1[3] in id_dict.keys():
                r=id_dict[q1[3]][0]+'/'+id_dict[q1[3]][1]
                print(r)
                print(q1[3])
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
                    ### Extract frequency
                    c_freq = hdf.get('/UniqueGlobalKey/context_tags/')
                    c_freq = (c_freq.attrs['sample_frequency']).decode('utf-8')
                    raw_fastq=(Fastq_data.value).decode('utf-8')
                    fastq_decoded=raw_fastq.split('\n')
                except AttributeError:
                    continue           

            # #################### Shifted to helper function module ################################

                final_eves=eH.event_scrapper(events)
                seq_no=3

                for e, i in enumerate(final_eves):

                    seq_no=seq_no+int(i[1])
                    len_seq=len(''.join(fastq_decoded[1]))
                    a_seq_no=(len_seq-int(q1[2]))+1
                ##### Tail pass
                    if a_seq_no > 2 and a_seq_no < len(final_eves)-2:
                        if seq_no == a_seq_no:
                            f_e=f_events(final_eves,e)

                            if len(f_e) != 0:
                                start=[]
                                end=[]
                                for s in f_e:
                                    print(s)
                                    for t in range(5):
                                        start.append(s[t][2])
                                        end.append(s[t][4])
                                        print(s[t][2])
                                print(start[2])
                                print(end[2])          
                                min_st=min(start)
                                max_stl=(max(end)-min(start))+1
                                sig='_'.join(map(str, raw_signal[min_st:][:max_stl]))
                                print(id_dict[q1[3]][1]+' '+i[0]+' '+q1[1]+'_'+q1[2]+' '+sig)
                                f.write(id_dict[q1[3]][1]+' '+i[0]+' '+q1[1]+'_'+q1[2]+' '+sig+'\n')
                            
