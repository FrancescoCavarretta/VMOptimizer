import numpy as np
import sys

filename = sys.argv[sys.argv.index('--filename')+1]
sort_flag = '--sorted' in sys.argv


# load parameters
inputs = list(numpy.load(filename, allow_pickle=True).tolist().items())

# sort in descending order by errors
if sort_flag:
    _inputs = inputs

    # sorting
    sorted_inputs_map = []
    for k, v in _inputs.items():
        err = np.max(np.abs(np.array(v['error'].values())))
        sorted_inputs_map.append((err, k))
    sorted_inputs_map = sorted(sorted_inputs_map)

    # inputs
    inputs = [ (k, _inputs[k]) for _, k in sorted_inputs_map ]
    
    del sorted_inputs_map, _inputs


    
    
                       

import sys
import bluepyopt
import os
from datetime import datetime
import CellEvalSetup 
import csv
import numpy as np
import collections
import matplotlib.pyplot as plt
import numpy
import time

def plot_responses(responses, dirname=''):
    # Select and sort reponses
    stim_names = [name for name in sorted(evaluator.fitness_protocols.keys()) ]
    sel_resp = collections.OrderedDict()
    for name in stim_names:
        sel_resp[name] =  responses["."+name+".soma.v"]

        
    for index, (resp_name, response) in enumerate(sorted(sel_resp.items())):
        fig = plt.figure()
        plt.plot(response['time'], response['voltage'])
        plt.ylabel('V$_m$ (mV)', fontsize = 'small')
        plt.xlabel('Time (ms)', fontsize = 'small')
        fig.show()
        plt.savefig(dirname+('fig_%s-%g.png'%(resp_name,index)))





scores = {}


halloffame = sorted( list( .items() ) )

import neuron

for i in range(len(halloffame)):
    key = halloffame[i][0]
    if key[4] != int(sys.argv[-1]) or key[2] != int(sys.argv[-2]):
        continue

    
    cfg = halloffame[i][1][0]
    obj = halloffame[i][1][1]
    etype = sys.argv[-4] 

    
    evaluator   = CellEvalSetup.evaluator.create(etype)

    if type(cfg) == tuple:
        dict_config = evaluator.param_dict(cfg)
    else:
        dict_config = cfg

    
    
    

    try:
        dict_obj    = evaluator.objective_dict(obj)
    except:
        dict_obj    = None
        
    scoretot_nsg = numpy.sum(obj)
    
    for k, v in dict_config.items():
        print (k, v)

    
    evaluator   = CellEvalSetup.evaluator.create(etype)
    print ("I=", i)
    t0 = datetime.now()
    responses = evaluator.run_protocols(
        protocols=evaluator.fitness_protocols.values(),
        param_values=dict_config)
    print("Simulation took {}.".format(datetime.now()-t0))


    dirname = etype + ('_directory-' + str(int(sys.argv[-1])) + '-' + str(int(sys.argv[-2])) + '/') 
    os.system('mkdir ' + dirname)
    plot_responses(responses, dirname=dirname)



    scoretot = 0.
    objectives = evaluator.fitness_calculator.calculate_scores(responses)

    
    for k, v in objectives.items():
        scoretot +=
