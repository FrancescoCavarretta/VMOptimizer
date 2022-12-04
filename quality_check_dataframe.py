import numpy as np
import sys
import eFELExt
import pandas as pd
import multiprocessing
import warnings

warnings.simplefilter('ignore')

def get_entry(data, cfg, i):
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
      if r is None:
        print(i, 'has a none entry', k)
        return pd.DataFrame()
      t = r['time']
      v = r['voltage']

      idx = t >= 1000
      t = t[idx]
      v = v[idx]


      trace = {
        'T':t,
        'V':v,
        'stim_start':[2000.0],
        'stim_end':[2000.0 + dur]
        }

      # set the threshold
      eFELExt.efel.setThreshold(-20.0 if entry['protocol']  == 'fi' else -35)

      # extract features
      entry.update( eFELExt.getFeatureValues(trace, ['AP_count', 'AP_count_before_stim', 'AP_count_after_stim', 'voltage_base', 'voltage_after_stim']) )

      # append
      efel_df = pd.concat([efel_df, pd.DataFrame(entry, index=[0])])

    return efel_df



if __name__ == '__main__':
  

  filename_cfg = sys.argv[sys.argv.index('--config')+1]
  filename_out_fmt = sys.argv[sys.argv.index('--sim-output')+1]
  filename_out_efel = sys.argv[sys.argv.index('--efel-output')+1]
  
  configurations = list(np.load(filename_cfg, allow_pickle=True).tolist().items())

  args = []

  for i, cfg in enumerate(configurations):

    data = list(np.load(filename_out_fmt % i, allow_pickle=True).tolist().items())

    # all arguments
    args.append((data, cfg, i))

    print ('neuron', i, 'done')


  efel_df = pd.DataFrame()
  pool = multiprocessing.Pool()
  results = pool.starmap(get_entry, args)
  
  for i, entry in enumerate(results):
    efel_df = pd.concat([efel_df, entry])
    print (i, 'entry done')
    
  pool.terminate()
  efel_df.to_csv(filename_out_efel)
