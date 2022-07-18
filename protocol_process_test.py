if __name__ == '__main__':
  import CellEvalSetup
  import numpy as np
  import sys


  param_file = sys.argv[sys.argv.index('--param_file')+1] # parameters
  response_file = sys.argv[sys.argv.index('--response_file')+1] # parameters
  coreneuron_active = '--coreneuron' in sys.argv
  verbose = '--verbose' in sys.argv
  
  try:
    index = int(sys.argv[sys.argv.index('--index')+1])
  except:
    index = None

 # load parameters
  param = np.load(param_file, allow_pickle=True).tolist()

  try:
    if index is None:
      index = 0
    key, vals = list(param.items())[index]
    etype = key[0] # etypes
    param = vals['parameter']
  
    # print errors and parameters
    if verbose:
      print ('Errors:')
      for x in vals['error'].items():
        print ('\t%s\t%f' % (x[0], abs(x[1])))
      print()
      print ('Param:')
      for x in vals['parameter'].items():
        print ('\t%s\t%f' % x)
      print()
      
  except:
    etype = sys.argv[sys.argv.index('--etype')+1]
    
  # create the evaluator for running the protocols
  evaluator = CellEvalSetup.evaluator.create(etype, coreneuron_active=coreneuron_active, use_process=False)


  
  # get the responses
  responses = evaluator.run_protocols(
    protocols=evaluator.fitness_protocols.values(),
    param_values=param)


  x = responses['.Step240_2000ms.soma.v']
  t = x['time'].to_numpy()
  v = x['voltage'].to_numpy()
  idx = t > 100
  trace = {'T':t[idx], 'V':v[idx], 'stim_start':[800], 'stim_end':[2800]}
  import eFELExt
  import efel
  efel.setThreshold(-20.)
  print ( eFELExt.getFeatureValues(trace, ['AP_count_after_stim']) )

  import evaluator
  ev=evaluator.eFELFeatureExtra('test',
            efel_feature_name='AP_count_after_stim',
            recording_names={'':'.Step240_2000ms.soma.v'},
            stim_start=800,
            stim_end=2800,
            exp_mean=0.0,
            exp_std=0.01,
            threshold=-20.0,
            int_settings={'strict_stiminterval':False},
            force_max_score=True,
            max_score=250.)
  print ( 'score', ev.calculate_score(responses) )

  # store the responses
  np.save(response_file, responses, allow_pickle=True)


