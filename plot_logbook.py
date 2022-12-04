import time
import sys
import numpy as np
import pickle
try:
  import matplotlib.pyplot as plt
  matplotlib_avail = True
except:
  matplotlib_avail = False

filename = sys.argv[-1]
with open(filename, 'rb') as fi:
    log = pickle.load(fi)['logbook']
print('# generations:', len(log))
    
x = []
y = []
z = []

for i in range(len(log)):
    x.append(i)
    y.append(log[i]['avg'])
    z.append(log[i]['std'])

x = np.array(x)
y = np.array(y)
z = np.array(z)

print (y)

if matplotlib_avail:
  plt.fill_between(x, y-z, y+z)
  plt.plot(x, y, color='red')

  plt.xlabel('Generation')
  plt.ylabel('Fitness')

  plt.ylim([0, 10000])
  plt.show()
