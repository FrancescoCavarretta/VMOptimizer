if __name__ == '__main__':
    import multiprocessing
    import os
    import sys
    import numpy as np
    filenamein = sys.argv[sys.argv.index('--input')+1]
    filenameout = sys.argv[sys.argv.index('--output')+1]

    cfg = list(np.load(filenamein, allow_pickle=True).tolist().items())
    n = len(cfg)
    
    pool = multiprocessing.Pool()
    args = [ ('python3 protocol_process.py --etype %s_quality_check --param_file %s --index %d --response_file %s_%d.npy' % (cfg[i][0][0], filenamein, i, filenameout, i), ) for i in range(n) ]
    pool.starmap(os.system, args)
    pool.terminate()
