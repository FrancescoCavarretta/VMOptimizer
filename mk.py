fmt = '#!/bin/sh\n' + \
	'#SBATCH -o scheduler_stdout_%s_%d.txt\n' + \
	'#SBATCH -e scheduler_stderr_%s_%d.txt\n' + \
	'#SBATCH --partition=compute           # submit to the large queue for jobs > 256 nodes\n' + \
	'#SBATCH -J %s_%d       # Job name\n' + \
	'#SBATCH -t 24:00:00         # Run time (hh:mm:ss) - 1.5 hours\n' + \
	'#SBATCH --mail-user=francesco.cavarretta@emory.edu\n' + \
	'#SBATCH --mail-type=begin\n' + \
	'#SBATCH --mail-type=end\n' + \
	'#SBATCH -A emu112\n' + \
	'#SBATCH --nodes=1              # Total number of nodes requested (16 cores/node)\n' + \
	'#SBATCH --ntasks-per-node=128             # Total number of mpi tasks requested\n' + \
	'#SBATCH --mem=128G\n' + \
	'module load cpu/0.15.4\n' + \
	'module load gcc/10.2.0\n' + \
	'module load python/3.8.5\n' + \
	'export PYTHONPATH=$PYTHONPATH:/home/fcavarr/.local/lib/python3.8/site-packages\n' + \
	'cd %s\n' + \
	'python3 thalamocortical-cell_opt.py --continue %s %d 100 100\n'

for i in range(15):
	for filename, mname in [ ('les', 'lesioned_719'), ('con', 'control_719') ]:
		with open(filename + '_' + str(i) + '.sh', 'w') as fo:
			fo.write(fmt % (mname, i, mname, i, mname, i, '/home/fcavarr/VMOptimizer', mname, i))
