import numpy as np
import sys
filenamein = sys.argv[sys.argv.index('--input')+1]
filenameout = sys.argv[sys.argv.index('--output')+1]

data = np.load(filenamein, allow_pickle=True).tolist()

'''for k in list(data.keys()):
  if k[0].startswith('lesioned'):
    data[k]['parameter']['gmax_iM.all'] *= 37.1
  else:
    del data[k]'''

for k in list(data.keys()):
  if k[0].startswith('lesioned'):
    data[k]['parameter']['gmax_iM.all'] *= 37.1 * 1.25
  else:
    del data[k]

np.save(filenameout, data, allow_pickle=True)
