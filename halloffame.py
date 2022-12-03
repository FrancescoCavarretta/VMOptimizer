class HistoryCheck:
  """
  Extract the hall-of-fames with all the errors below threshold
  """
  def __init__(self, filenames, max_score_thresh, other_thresh={}):
    import json

    self.filenames = filenames
    self.max_score_thresh = max_score_thresh
    self.other_thresh = other_thresh



  def get(self):
    '''
    Get the hall-of-fame
    '''
    tracked_solution = set()
    ret = {}
    for filename in self.filenames:
      ret.update(self._get(filename, tracked_solution))
    return ret

  
  
  def _get(self, filename, tracked_solution):
    import numpy
    import pickle
    import CellEvalSetup
    
    # split the simulation name in type and extract the seed
    etype, seed = filename.replace('.pkl', '').split('_checkpoint_')
    seed = int(seed)

    # instantiate evaluator
    evaluator = CellEvalSetup.evaluator.create(etype)
    
    # read file
    with open(filename, 'rb') as fi:
      log = pickle.load(fi)

    # go over all the solutions
    ret = {}
    for k, param in log['history'].genealogy_history.items():
      errors = evaluator.objective_dict(log['history'].genealogy_history[k].fitness.wvalues)


      _errors = errors.copy()
      flag_err = False
      for k_err, v_err in _errors.copy().items():
        for k_err_ref, th_err_ref in self.other_thresh.items():
          if k_err_ref in k_err:
            del _errors[k_err]
            if abs(v_err) > th_err_ref:
              flag_err = flag_err or True 
      
      if numpy.max(numpy.abs(list(_errors.values()))) > self.max_score_thresh:
        # check each error
        flag_err = flag_err or True

      # pass this configuration
      if flag_err:
        continue
              
          
      if tuple(param) not in tracked_solution:
        tracked_solution.add(tuple(param))
        ret.update({(etype, k, seed):{
          'error':errors,
          'parameter':evaluator.param_dict(param)
          }})
    return ret





if __name__ == '__main__':
  import sys
  import numpy
  
  thresh = float(sys.argv[sys.argv.index('--threshold') + 1])
  output  = sys.argv[sys.argv.index('--output') + 1]

  filenames = []
  for s in sys.argv[sys.argv.index('--input')+1:]:
    if s.startswith('--'):
      break
    filenames.append(s)

  other_thresh = {}
  for s in sys.argv:
    if s.startswith('--thresh-'):
      k, v = s.replace('--thresh-', '').split('=')
      v = float(v)
      other_thresh[k] = v
    
  hc = HistoryCheck(filenames, thresh, other_thresh=other_thresh)
  sol = hc.get()
  print (len(sol), 'solutions found')
  numpy.save(output, sol, allow_pickle=True)
    
