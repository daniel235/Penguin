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

        sam_file.append(u1[0]+' '+u1[1]+' '+u1[2]+' '+u1[3]+' '+u1[4]+' '+u1[5]+' '+u1[6] )

    total=len(sam_file)
    print("Sam file read successfully..starting coordinate extraction...")

#   802 1489

    mod_d=dict()

    for e in locs:
        #split columns
        e1=e.split( )
        if e1[5] == '+':
            #chromosome location
            chr=''.join(e1[0])
            chr_loc=''.join(e1[1])
            #add location to chromosome modified dictionary
            if chr in mod_d:
                mod_d[chr].append(int(chr_loc))
            else:
                mod_d[chr] = [int(chr_loc)]


     ### define output filename
    with open("./Data/pstrand_chr_modification_coors.txt", "a") as f:
        ### loop through samfile ####
        for t, i in enumerate(sam_file):
            if not i.startswith('@'):
                i1=i.split()
                #chrm num
                s_chr=''.join(i1[2])
                #position
                s_chr_s=''.join(i1[3])
                #cigar, position
                coordinates,gstop=cigar_parse(i1[5],int(i1[3]))
                try:
                    #chrm num
                    for chr_loc in mod_d[s_chr]:
                        if int(chr_loc)-2 >= int(i1[3]) and int(chr_loc)+2 <= int(i1[3])+gstop:
                            for coord in coordinates:
                                if int(coord[0]) <= int(chr_loc) and int(coord[1]) >= int(chr_loc):
                                    #sam file range of coordinates
                                    genomic_coor=list(range(int(coord[0]),int(coord[1])+1))
                                    #print(genomic_coor)
                                    seq_coor=list(range(int(coord[2]),int(coord[3])+1))
                                    # print(seq_coor)
                                    i_gc=genomic_coor.index(int(chr_loc))
                                    i_sc=seq_coor[i_gc]
                                    f.write(str(s_chr)+' '+str(chr_loc)+' '+str(i_sc)+' '+str(i1[0])+'\n')

                except KeyError:
                    continue
