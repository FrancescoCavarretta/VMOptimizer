if __name__ == '__main__':
  import CellEvalSetup
  import numpy as np
  import sys

  etype = sys.argv[sys.argv.index('--etype')+1] # etypes
  param_file = sys.argv[sys.argv.index('--param_file')+1] # parameters
  response_file = sys.argv[sys.argv.index('--response_file')+1] # parameters
  coreneuron_active = '--coreneuron' in sys.argv

 # load parameters
  param = np.load(param_file, allow_pickle=True).tolist()
  
  # create the evaluator for running the protocols
  evaluator = CellEvalSetup.evaluator.create(etype, coreneuron_active=coreneuron_active, use_process=False)
  
  # get the responses
  responses = evaluator.run_protocols(
    protocols=evaluator.fitness_protocols.values(),
    param_values=param)

  # store the responses
  np.save(response_file, responses, allow_pickle=True)
