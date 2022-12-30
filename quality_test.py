from mpi4py import MPI
import numpy as np
import os

def main(cfg, filenameout, no_quality_test, bias_perc):
    if MPI.COMM_WORLD.Get_rank() == 0:
        return controller(cfg, filenameout)
    else:
        return run(bias_perc, no_quality_test)


def controller(filenamein, filenameout):
    # open configurations
    cfg = np.load(filenamein, allow_pickle=True).tolist()
    
    mpi_comm = MPI.COMM_WORLD

    # consumer available for running simulations
    free_ranks = list(range(1, mpi_comm.Get_size()))

    cfg_keys = sorted(list(cfg.keys()))
    cfg_keys_to_use = cfg_keys + []

    print('Running')

    while len(cfg_keys_to_use):
        # occupy all the ranks
        while len(free_ranks) and len(cfg_keys_to_use):
            try:
                k = cfg_keys_to_use.pop()
            except IndexError:
                break

            # assemble message
            message = {'key':k, 'parameter':cfg[k]['parameter'], 'filenamein':filenamein, 'filenameout':filenameout, 'index':cfg_keys.index(k)}
            rank = free_ranks.pop()

            # submit
            mpi_comm.send(obj=message, dest=rank, tag=0)
            
        # receive the message
        message = mpi_comm.recv()

        #print('file saved')
        free_ranks.append(message['rank'])

    # processes left
    while len(free_ranks) < mpi_comm.Get_size() - 1:
        # receive the message
        message = mpi_comm.recv()

        #print('file saved')
        free_ranks.append(message['rank'])

    # send termination signal to all
    for rank in range(1, mpi_comm.Get_size()):
        mpi_comm.send(obj=None, dest=rank, tag=0)

    print('finished')


def run(bias_perc, no_quality_test=False):
    mpi_comm = MPI.COMM_WORLD

    rank = mpi_comm.Get_rank()

    # receive a message
    message = mpi_comm.recv(source=0, tag=0)

    while message:
        # pack output
        cfg_key = message['key']
        output = None
        if no_quality_test:
            os.system('python3 protocol_process.py --atol 1e-4 --etype %s --param_file %s --index %d --response_file %s_%d.npy' % (message['key'][0], message['filenamein'], message['index'], message['filenameout'], message['index']))
        else:
            os.system('python3 protocol_process.py --atol 1e-4 --etype %s_quality_check_%d --param_file %s --index %d --response_file %s_%d.npy' % (message['key'][0], bias_perc, message['filenamein'], message['index'], message['filenameout'], message['index']))
        dict_message = dict(output=output, rank=rank, key=cfg_key)

        # send out
        mpi_comm.send(obj=dict_message, dest=0, tag=0)
        
        # receive a message
        message = mpi_comm.recv(source=0, tag=0)
    




if __name__ == '__main__':
    import sys

    filenamein = sys.argv[sys.argv.index('--input')+1]
    filenameout = sys.argv[sys.argv.index('--output')+1]
    no_quality_test = '--no-quality' in sys.argv
    if no_quality_test:
      bias_perc = None
    else:
      bias_perc = int(sys.argv[sys.argv.index('--bias-perc')+1])
    
    main(filenamein, filenameout, no_quality_test, bias_perc)

    sys.exit(0)


