#################### Shifted to helper function module ################################
##### Extract the kmer and its signals


import math
import os 

def event_scrapper(file):
    bk=0
    kmer=[]
    times=[]
    evenlens=[]
    s_moves=[]

    for k, i in enumerate(file):
        kmers=[]
        time=[]	
        evenlen=[]
        s_move=[]

        kmers.append(i[4])
        if k == bk:
            file1=file
            for r, s in enumerate(file1):
                if r == k:
                    if s[4] == i[4] and int(s[5]) != 0:
                        time.append(s[2])
                        s_move.append(s[5])
                        evenlen.append(int(s[3]))
                if r > k:
                    if s[4] == i[4]  and int(s[5]) == 0:
                        time.append(s[2])
                        s_move.append(s[5])
                        evenlen.append(int(s[3]))
                    if r > k and int(s[5]) != 0:
                        bk=r
                        break

            for v in kmers:
                kmer.append(v)
            s_moves.append(s_move)  
            times.append(time)
            time=[]
            s_move=[]
            evenlens.append(evenlen[-1:])

            
    f_events=[]
    for c, r, d, t in zip(kmer,s_moves,times,evenlens):
        d=list(map(int,d))
        if c != "model_state":
            t=', '.join(map(str, t))
            f_events.append([c.decode('utf-8'),max(r),min(d),max(d),max(d)+int(t)])

    return f_events
####################################################


def f_events(final_eves,x):
    asd=[]

    for t, v in enumerate(zip(final_eves[:-1],final_eves[1:],final_eves[2:],final_eves[3:],final_eves[4:])):
        if t > 2 and t <= len(final_eves)-2:
            if t == x-2:
                asd.append(v)
    return asd
