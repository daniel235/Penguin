import re, os


def cigar_parse(cigar,start):
    insertions = []
    alignments = []
    aligns=[]

    pattern = re.compile('([MIDNSHPX=])')
    values = pattern.split(cigar)[:-1] ## turn cigar into tuple of values
    paired = (values[n:n+2] for n in range(0,len(values),2)) ## pair values by twos
    i = 0 ## alignment coordinate index
    g = start ## genomic coordinate index
    gstop=0
    for pair in paired:
        l = int(pair[0]) ## length of CIGAR event
        t = pair[1] ## type of CIGAR event
        if t == 'M': ## if match, return consecutive coordinates
            alignments.append((g, g+i+l-i,(i, i + l))) ## (genomic offset, (alignment.start, alignment.end))
            aligns.append((g, g+i+l-i, i, i+l)) ## (genomic offset, (alignment.start, alignment.end))
            i += l
            g += l
            gstop=g+i+l-i
        elif t == 'D': ## skip 'l' number of coordinates in reference
            g += l
        elif t == 'I': ## insertion of 'l' length
            insertions.append((i, i + l))
            i += l
        elif t == 'N': ## skipped region from the reference
            g += l
        elif t == 'S': ## soft clipping (clipped sequences present in SEQ)
            i += l
        elif t == 'H': ## hard clipping (clipped sequences NOT present in SEQ)
            pass
        elif t == 'P': ## padding (silent deletion from padded reference)
            pass
        elif t == '=': ## sequence match
            pass
        elif t == 'X': ## sequence mismatch
            pass

    return aligns, gstop



def extract_modified_coords(bedPath, samPath):
    locs=open(bedPath, 'r')
    sam_file=[]

    file3 = open(samPath, 'r')
    for u in file3:
        u1=u.split( )
        if len(u1) < 3:
            continue
        if u1[0] == '@SQ':
            continue

        #print("u1 ", u1)
        sam_file.append(u1[0]+' '+u1[1]+' '+u1[2]+' '+u1[3]+' '+u1[4]+' '+u1[5]+' '+u1[6] )

    total=len(sam_file)
    print("total sam file ", sam_file)
    print("Sam file read successfully..starting coordinate extraction...")

    mod_d=dict()

    dict_len=0
    mods=[]
    for e in locs:
        #split columns
        e1=e.split( )
        print("e1 ", e1)
        print("e1 5 ", e1[5])
        if e1[5] == '+':
            print("in positive")
            #chromosome location
            mods.append(e1[0]+'_'+e1[1])
            chr=''.join(e1[0])
            print("chr ", chr)
            chr_loc=''.join(e1[1])
            #add location to chromosome modified dictionary
            if chr in mod_d:
                mod_d[chr].append(int(chr_loc))
            else:
                mod_d[chr] = [int(chr_loc)]

    for key, value in mod_d.items():
        dict_len=dict_len+len(value)

    #file2=open('pstrand_m5C_chr_Modification_coors_ns.txt','a') ### define output filename
    with open("./Data/pstrand_chr_modification_coors.txt", "a") as f:
        c=0
        ### loop through samfile ####
        for t, i in enumerate(sam_file):
            if not i.startswith('@'):
                i1=i.split()
                s_chr=''.join(i1[2])
                s_chr_s=''.join(i1[3]) 
                coordinates,gstop=cigar_parse(i1[5],int(i1[3]))
                try:
                    for v in mod_d[s_chr]:
                        if int(v)-2 >= int(i1[3]) and int(v)+2 <= int(i1[3])+gstop:
                            for r in coordinates:
                                if int(r[0]) <= int(v) and int(r[1]) >= int(v): 
                                    genomic_coor=list(range(int(r[0]),int(r[1])+1))
                                    #print(genomic_coor)
                                    seq_coor=list(range(int(r[2]),int(r[3])+1))
                                    # print(seq_coor)
                                    i_gc=genomic_coor.index(int(v))
                                    i_sc=seq_coor[i_gc]
                                    print("coord write")
                                    f.write(str(s_chr)+' '+str(v)+' '+str(i_sc)+' '+str(i1[0])+'\n')
                                    
                except KeyError:
                    continue

            c=c+1
            print(c ,total)
