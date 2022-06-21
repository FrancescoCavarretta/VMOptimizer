#!/usr/bin/env python
# coding: utf-8

# # Optimization of burst and tonic firing in thalamo-cortical neurons

# ____
# 
# This notebook illustrates how to **setup** and **configure optimisations** presented in the following paper:
# 
# Iavarone, Elisabetta, Jane Yi, Ying Shi, Bas-Jan Zandt, Christian O'Reilly, Werner Van Geit, Christian Rössert, Henry Markram, and Sean L. Hill. ["Experimentally-constrained biophysical models of tonic and burst firing modes in thalamocortical neurons."](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006753).
# 
# Author of this script: Elisabetta Iavarone @ Blue Brain Project
# ___
# 
# The models were constrained by using the **experimental data** from Jane Yi, Ying Shi and Henry Markram at the [LNMC, EPFL](https://www.epfl.ch/labs/markram-lab/).
# 
# The morphologies will be available on NeuroMorpho.org under the
# ODC Public Domain Dedication and Licence (PDDL) https://opendatacommons.org/licenses/pddl/1.0/
# _____
# 
# This notebook makes use of scripts to automatically setup the optimisation, stored in the *config* and *setup* subfolders. To learn more about concepts such as *mechanisms*, *cell template*, *cell evaluator*, we suggest to go through the [L5PC example](https://github.com/BlueBrain/BluePyOpt/blob/master/examples/l5pc/L5PC.ipynb).
# _____
# 
# **If you use methods or data presented in this notebook we ask to cite the following publications:**
# 
# Iavarone, Elisabetta, Jane Yi, Ying Shi, Bas-Jan Zandt, Christian O'reilly, Werner Van Geit, Christian Rössert, Henry Markram, and Sean L. Hill. "Experimentally-constrained biophysical models of tonic and burst firing modes in thalamocortical neurons." [BioRxiv (2019): 512269](https://www.biorxiv.org/content/10.1101/512269v3).
# 
# Van Geit, W., Gevaert, M., Chindemi, G., Rössert, C., Courcol, J. D., Muller, E. B., ... & Markram, H. (2016). BluePyOpt: leveraging open source software and cloud infrastructure to optimise model parameters in neuroscience. [Frontiers in neuroinformatics, 10, 17](https://www.frontiersin.org/articles/10.3389/fninf.2016.00017/full).
# 
# ___
# 
# 
# **If you re-use any file from the *mechanisms* folder you should also cite the associated publication.**
# 
# See license file for details.
# 
# ___

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

import bluepyopt
import os

import pprint
pp = pprint.PrettyPrinter(indent=2)


# ## Set up the cell model and the cell evaluator

# A cell evaluator can be easily created by specifing the desired electrical type (e-type).
# 
# A cell model is part of the cell evaluator and it is built by specifying a **morphology**, **mechanisms**, i.e. the ion channel models and the **bounds for the parameter values** (i.e. the densities of the ion channels)

# In[2]:


# Import scripts for setting up the cell model and cell evaluator
import CellEvalSetup 

# Library to visualize and analyse morphologies 
import neurom # https://github.com/BlueBrain/NeuroM
import neurom.viewer

etype = "cAD_ltb" # or cNAD_ltb 

evaluator = CellEvalSetup.evaluator.create(etype)

neurom.viewer.draw(neurom.load_neuron(evaluator.cell_model.morphology.morphology_path))
print(evaluator.cell_model)


# ## Run an optimisation
# 
# Once we have created the cell evaluator, we can run an optimisation. During the optimisation different parameter values will be evaluated, by running different **stimulation protocols** and recording the **voltage responses** of the models. 
# 
# The algorithm will try minimise the difference between the **electrical features** measured from the voltage responses in the model and the features extracted from the experimental data.

# In[3]:


seed = 0 # Number to initialize the pseudorandom number generator

opt = bluepyopt.optimisations.DEAPOptimisation(
    evaluator=evaluator,
    map_function=map, # The map function can be used to parallelize the optimisation
    seed=seed,
    eta=10., mutpb=1.0, cxpb=1.0)


# As a proof of concept, we run an optimisation with a small number of individuals (n = 2) and generations (n = 2); this step will require some minutes. Typically this optimisation was run with 100 individual for 100 generations. At the end we obtain the "Hall of Fame", where the first individual is the best model.
# 
# Before we create a folder to save the results.

# In[ ]:


get_ipython().system('nrnivmodl mechanisms # Compile NEURON .mod files stored in the "mechanisms" folder')

if not os.path.exists('checkpoints'):
    os.mkdir('checkpoints')

final_pop, halloffame, log, hist, = opt.run(max_ngen=2,
        offspring_size=2,
        cp_filename='checkpoints/checkpoint.pkl');


# In[6]:


print("\nExample of one individual resulting from an optimisation run:\n")
print(halloffame[0])


# ## Analyse optimisation results
# 
# In this section you will see how to run simulations with models obtained after running a full optimisation.
# 

# In[7]:


import csv

with open('results/{}_params.csv'.format(etype)) as csvfile:
    rows = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    params = list(rows)


# Select one of the models and create the dictionary of parameters.

# In[8]:


modid = 62 # Or e.g. 78 for cNAD_ltb model shown in the paper, Fig. 4
param_dict = evaluator.param_dict(params[modid])
pp.pprint(param_dict)


# We can run a simulation with the parameters above and the current protocols which are part of the evaluator.

# In[9]:


from datetime import datetime

t0 = datetime.now()
responses = evaluator.run_protocols(protocols = evaluator.fitness_protocols.values(), param_values=param_dict)

print("Simulation took {}.".format(datetime.now()-t0))


# We can plot the model responses.

# In[11]:


import collections

def plot_responses(responses):
    # Select and sort reponses
    stim_names = [name for name in sorted(evaluator.fitness_protocols.keys()) 
                      if "hold" not in name and "RMP" not in name]
    sel_resp = collections.OrderedDict()
    for name in stim_names:
        sel_resp[name] =  responses["."+name+".soma.v"]
        
    fig, axes = plt.subplots(len(sel_resp), figsize=(5, 8), sharey = True)
    for index, (resp_name, response) in enumerate(sorted(sel_resp.items())):
        
        startid = 550 if "Step" in resp_name or "IV" or "Rin" in resp_name else 0 # Remove initial transient
        indices = response['time'] >= startid
        
        axes[index].plot(response['time'][indices]-startid, response['voltage'][indices],
                        color = "blue", lw = 0.75, alpha = 0.8)
        
        axes[index].set_ylabel('V$_m$ (mV)', fontsize = 'small')
        axes[-1].set_xlabel('Time (ms)', fontsize = 'small')
    fig.tight_layout()
    fig.show()
plot_responses(responses)


# We can evaluate the fitness of the model by computing its errors. Each error quantify how much the model deviates from the experimental features.

# In[12]:


objectives = evaluator.fitness_calculator.calculate_scores(responses)

def plot_objectives(objectives): 
    
    # Names for all the stimuli   
    stim_name = ['RMP', u'IV_-140', u'Rin_dep',  'hold_hyp', u'Step_200_hyp',  u'Step_150', 
             u'Step_200', u'Step_250', 'hold_dep']
    
    # Sort objectives
    obj_keys = [[key for key in objectives.keys() if key.split(".")[1] == stim] for stim in stim_name]
    obj_keys = [item for sublist in obj_keys for item in sublist][::-1] 
    obj_val = []
    for key in obj_keys:
        obj_val.append(objectives[key])
 
    ytick_pos = [x + 0.5 for x in range(len(obj_keys))]
    fig, ax = plt.subplots(figsize = (5.4,9), facecolor = 'white')
  
    ax.barh(ytick_pos,
              obj_val,
              height=0.5,
              align='center',
              color='blue',
              alpha=0.5)
    
    obj_keys = [CellEvalSetup.tools.rename_feat(name) for name in obj_keys]     
        
    ax.set_yticks(ytick_pos)
    ax.set_yticklabels(obj_keys, size='medium')
    ax.set_ylim(-0.5, len(obj_keys) + 0.5)
    ax.set_xlim([0,3])
      
    ax.set_xlabel("Distance from exp. mean (# STD)")
    ax.set_ylabel("Feature name")
    ax.xaxis.grid(True)
    fig.tight_layout()

plot_objectives(objectives)

