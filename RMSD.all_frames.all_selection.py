#!/mnt/lustre_fs/users/mjmcc/apps/python2.7/bin/python
##!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# ----------------------------------------
# USAGE:
#

# ----------------------------------------
# PREAMBLE:

import MDAnalysis
from MDAnalysis.analysis.align import *
import sys
import os
import sel_list
from distance_functions import *

# ----------------------------------------
# VARIABLE DECLARATION

pdb_file = sys.argv[1]
traj = sys.argv[2]

flush = sys.stdout.flush
makedir = os.mkdir
changedir = os.chdir
terminal = os.system

# ----------------------------------------
# SUBROUTINES:

def ffprint(string):
        print '%s' %(string)
        flush()

# ----------------------------------------
# MAIN PROGRAM:
# LOADING IN THE BACKBONE TRAJECTORY
u = MDAnalysis.Universe('%s' %(pdb_file),'%s' %(traj))
# DECLARING THE ATOM SELECTIONS
u_all = u.select_atoms('all')
u_backbone = u.select_atoms('backbone')
u_beta = u.select_atoms('name CA and (resid 19:25 or resid 50:55 or resid 90:94 or resid 112:117 or resid 142:149 or resid 165:169 or resid 190:194 or resid 214:218 or resid 236:240 or resid 253:258 or resid 303:307)')

nSteps = len(u.trajectory)
ffprint('Number of Steps: %d' %(nSteps))
nSel = len(sel_list.sel)

# BEGIN SELECTION/TRAJECTORY ANALYSIS
for i in range(nSel):
	selection = sel_list.sel[i][1]
	u_sel = u.select_atoms(selection)
	makedir('%s' %(sel_list.sel[i][0]))
	changedir('%s' %(sel_list.sel[i][0]))
	out = open('%s.rmsd_matrix.dat' %(sel_list.sel[i][0]), 'w')

	for j in range(nSteps-1):
		u.trajectory[j]
		u_all.translate(-u_backbone.center_of_mass())
		pos0 = u_beta.coordinates()
		pos1 = u_sel.coordinates()

		for k in range(j+1,nSteps):
			u.trajectory[k]
			# ALIGN THE BETA SHEETS
			R, rmsd = rotation_matrix(u_beta.coordinates(),pos0)
			# APPLY THE ROTATION MATRIX TO THE ATOMS OF INTEREST
			u_all.rotate(R)
			# CALC THE RMSD VALUE BETWEEN FRAMES
			rmsd = RMSD(u_sel.coordinates(),pos1)
			# PRINT THE RESULTS TO THE OUTPUT FILE
			out.write('%d   %d    %f \n' %(j,k,rmsd))
	out.close()
	changedir('..')

