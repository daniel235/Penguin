import h5py, os


def parse_fast5_ids(fast5Path):
    with open("Fast5_ids.txt", "w+") as f:
        for dirpath, dirs, files in os.walk(fast5Path):
            for filename in files:
                if filename.endswith(".fast5"):
                    hdf = h5py.File(dirpath+'/'+filename, 'r+')

                    #extract signal
                    fast5_p_id=hdf.get('Raw/Reads/')
                    sas=''.join(list(fast5_p_id.keys()))

                    fast5_ids=hdf.get('Raw/Reads/'+sas+'/')
                    fast5_ids=fast5_ids.attrs['read_id']

                    read_id_v=fast5_ids.decode('utf-8')
                    fast5_u_ids=hdf.get('UniqueGlobalKey/tracking_id/')
                    fast5_u_ids=fast5_u_ids.attrs['run_id']
                    run_id_v=fast5_u_ids.decode('utf-8')
                    print(filename+' '+read_id_v+' '+run_id_v)
                    f.write(dirpath+' '+filename+' '+read_id_v+' '+run_id_v+'\n')
                    