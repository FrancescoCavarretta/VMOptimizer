
import CellEvalSetup

def get_responses(etype, param):
    """
    Evaluate a set of parameters
    """
    
    # create the evaluator for running the protocols
    evaluator = CellEvalSetup.evaluator.create(etype)
    
    # get the responses
    responses = evaluator.run_protocols(
      protocols=evaluator.fitness_protocols.values(),
      param_values=param)

    # clean the memory
    del evaluator

    return responses

  
if __name__ == '__main__':
  import numpy as np
  import sys
  import neuron
#  neuron.h.CVode().atol(1e-10)

  no_simulation = '--no-sim' in sys.argv

  if '--atol' in sys.argv:
    neuron.h.CVode().atol(float(sys.argv[sys.argv.index('--atol')+1]))
  
  param_file = sys.argv[sys.argv.index('--param_file')+1] # parameters
  if not no_simulation:
    response_file = sys.argv[sys.argv.index('--response_file')+1] # parameters
  verbose = '--verbose' in sys.argv or no_simulation
  recalculate_errors = '--recalculate-errors' in sys.argv
  
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
    pass
  
  if not no_simulation:
    # get eType
    try:
      etype = sys.argv[sys.argv.index('--etype')+1]
    except:
      pass
  

    # generate responses
    responses = {'param':param, 'responses':get_responses(etype, param), 'key':key}


    # store the responses
    np.save(response_file, responses, allow_pickle=True)
    
    if recalculate_errors:
    # print feature values
      for k, v in evaluator.evaluate_with_dicts(param_dict=param, target='values').items():
        print(k, '\t', v)
