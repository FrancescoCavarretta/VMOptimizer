import numpy as np
import sys
import eFELExt
import pandas as pd
import multiprocessing
import warnings

warnings.simplefilter('ignore')

def get_entry(data, cfg):
  efel_df = pd.DataFrame()
  
  for k, r in data:
    # data
    entry = { 'etype' :cfg[0][0],
              'cellid':cfg[0][1],
              'seed'  :cfg[0][2] }

    # state
    entry['state'] = 'normal' if 'control' in entry['etype'] else '6ohda'

    # simulation configs
    sim_type, sim_cfg = k[1:].replace('ms.soma.v', '').split('Step')
    
    amp_tk, dur_tk = sim_cfg.split('_')
    amp = int(amp_tk)
    dur = int(dur_tk)
    
    entry['protocol'] = { '':'fi', 'Sag':'rmih', 'Rebound':'tburst' }[sim_type]
    entry['amplitude'] = amp
    entry['duration'] = dur

    # extract info
    t = r['time']
    v = r['voltage']

    idx = t > 100
    t = t[idx]
    v = v[idx]


    trace = {
      'T':t,
      'V':v,
      'stim_start':[800.0],
      'stim_end':[800.0 + dur]
      }

    # set the threshold
    eFELExt.efel.setThreshold(-20.0 if entry['protocol']  == 'fi' else -34.75)

    # extract features
    entry.update( eFELExt.getFeatureValues(trace, ['AP_count', 'AP_count_before_stim', 'AP_count_after_stim', 'voltage_base', 'voltage_after_stim']) )

    # append
    efel_df = pd.concat([efel_df, pd.DataFrame(entry, index=[0])])

  return efel_df


if __name__ == '__main__':
  

  filename_cfg = 'hof_3sd.npy' #sys.argv[sys.argv.index('--config')+1]
  filename_out_fmt = 'output_%d.npy' #sys.argv[sys.argv.index('--output')+1]

  configurations = list(np.load(filename_cfg, allow_pickle=True).tolist().items())

  args = []

  for i, cfg in enumerate(configurations):

    data = list(np.load(filename_out_fmt % i, allow_pickle=True).tolist().items())

    # all arguments
    args.append((data, cfg))

    print ('neuron', i, 'done')


  efel_df = pd.DataFrame()
  pool = multiprocessing.Pool()
  results = pool.starmap(get_entry, args)
  
  for i, entry in enumerate(results):
    efel_df = pd.concat([efel_df, entry])
    print (i, 'entry done')
    
  pool.terminate()
  efel_df.to_csv('qc_output.csv')
