import numpy as np
import sys
filenamein = sys.argv[sys.argv.index('--input')+1]
filenameout = sys.argv[sys.argv.index('--output')+1]

data = np.load(filenamein, allow_pickle=True).tolist()

#for k in list(data.keys()):
#  if k[0].startswith('control'):
#    del data[k]

gm_6ohda = np.mean([ data[k]['parameter']['gmax_iM.all'] for k in data.keys() if k[0].startswith('lesioned') ])
gm_control = np.mean([ data[k]['parameter']['gmax_iM.all'] for k in data.keys() if k[0].startswith('control') ])
factor = gm_control / gm_6ohda
factor = 40
print('factor', factor)

for k in list(data.keys()):
  if k[0].startswith('lesioned'):
    data[k]['parameter']['gmax_iM.all'] *= factor 
  else:
    del data[k]

np.save(filenameout, data, allow_pickle=True)
