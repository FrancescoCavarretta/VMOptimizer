import numpy as np
import sys
import eFELExt
import pandas as pd
import multiprocessing
import warnings

warnings.simplefilter('ignore')

def get_entry(filename, i):
#    print(filename, i)
    r = np.load(filename, allow_pickle=True).tolist()
    data, cfg = r['responses'], r['key']
    efel_df = pd.DataFrame()
#    print(r)    
    for k, r in data.items():
      # data
      entry = { 'etype' :cfg[0],
                'cellid':cfg[1],
                'seed'  :cfg[2] }

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
      
      # interpolation
      tp = np.linspace(1000, 5000, 4000)
      vp = np.interp(tp, t, v)
      idx = tp >= 1000
      t, v = tp[idx], vp[idx]

      trace = {
        'T':t,
        'V':v,
        'stim_start':[2000.0],
        'stim_end':[2000.0 + dur]
        }

      # set the threshold
      eFELExt.efel.setThreshold(-20.0 if entry['protocol']  == 'fi' else -35)

      # extract features
      entry.update( eFELExt.getFeatureValues(trace, ['adaptation_index2', 'AP_count', 'AP_count_before_stim', 'AP_count_after_stim', 'voltage_base', 'voltage_after_stim', 'voltage_deflection', 'AP_amplitude', 'AP1_amp', 'AP2_amp', 'fast_AHP', 'AHP_depth', 'AP_amplitude_change', 'sag_amplitude']) )

      # append
      efel_df = pd.concat([efel_df, pd.DataFrame(entry, index=[0])])
#    print(efel_df)
    return efel_df



if __name__ == '__main__':
  

  n_cfg = int(sys.argv[sys.argv.index('--n-config')+1])
  filename_out_fmt = sys.argv[sys.argv.index('--sim-output')+1]
  filename_out_efel = sys.argv[sys.argv.index('--efel-output')+1]
  if '--filter' in sys.argv:
    filter_keys = np.load(sys.argv[sys.argv.index('--filter')+1], allow_pickle=True).tolist()
  else:
    filter_keys = None

  args = []

  for i in range(n_cfg):
    try:
      data = np.load(filename_out_fmt % i, allow_pickle=True).tolist()
    except FileNotFoundError:
      print ('neuron', i, 'done with error')
      continue
    if filter_keys and data['key'] not in filter_keys:
      continue

    # all arguments
    args.append((filename_out_fmt % i, i))

    print ('neuron', i, 'done')


  efel_df = pd.DataFrame()
  pool = multiprocessing.Pool()
  chunksize = int(n_cfg / multiprocessing.cpu_count())
  if chunksize == 0: 
    chunksize = 1
  results = pool.starmap(get_entry, args, chunksize=chunksize)
  
  for i, entry in enumerate(results):
    efel_df = pd.concat([efel_df, entry])
    print (i, 'entry done')
    
  pool.terminate()
  efel_df.to_csv(filename_out_efel)
