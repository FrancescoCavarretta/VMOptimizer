import numpy as np
import sys
filenamein = sys.argv[sys.argv.index('--input')+1]
filenameout = sys.argv[sys.argv.index('--output')+1]

data = np.load(filenamein, allow_pickle=True).tolist()

for v in data.values():
  v['parameter']['gmax_iM.all'] = 1e-20

np.save(filenameout, data, allow_pickle=True)
