#!/mnt/lustre_fs/users/mjmcc/apps/python2.7/bin/python
##!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# ----------------------------------------
# USAGE:

# ----------------------------------------
# PREAMBLE:

import MDAnalysis
from MDAnalysis.analysis.align import *
import sys

# ----------------------------------------
# VARIABLE DECLARATION

ref = sys.argv[1]		# full protein reference structure...
traj_loc = sys.argv[2]		# pointer to the directories of the systems...
out = sys.argv[3]		# output file name w/ extension

selection = 'protein'
alignment = 'protein and name CA and (resid 20:25 or resid 50:55 or resid 73:75 or resid 90:94 or resid 112:116 or resid 142:147 or resid 165:169 or resid 190:194 or resid 214:218 or resid 236:240 or resid 253:258 or resid 303:307)'

grab_frame = 50 	#grab a frame every 50 frames (100 ps);

flush = sys.stdout.flush

sys = []
sys.append(['AMBER_apo', 21, 150])		#
#sys.append(['AMBER_atp', 51, 100])		#
#sys.append(['AMBER_ssrna', 51, 100])		#
#sys.append(['AMBER_ssrna_atp', 51, 100])	#
#sys.append(['AMBER_ssrna_adp_pi', 51, 100])	#
#sys.append(['AMBER_ssrna_adp', 51, 100])	#
#sys.append(['AMBER_ssrna_pi', 51, 100])		#

# ----------------------------------------
# SUBROUTINES:

def ffprint(string):
        print '%s' %(string)
        flush()

# ----------------------------------------
# MAIN PROGRAM:

ref = MDAnalysis.Universe('%s' %(ref))		
ref_align = ref.select_atoms(alignment)
ref_important = ref.select_atoms(selection)

ref_important.translate(-ref_important.center_of_mass())
ref_important.write('reference_structure.pdb')

ref_atoms = len(ref_important.atoms)
pos0 = ref_align.positions

out1 = open('frames.dat', 'w')
with MDAnalysis.Writer('%s' %(out), ref_atoms) as W:
	for i in range(len(sys)):
		ffprint('Loading system %s' %(sys[i][0]))
		u = MDAnalysis.Universe('%s%s/truncated.pdb' %(traj_loc, sys[i][0]))	
		
		u_all = u.select_atoms('all')
		u_align = u.select_atoms(alignment)
		u_sel = u.select_atoms(selection)
		nAtoms = len(u_sel.atoms)
		if nAtoms != ref_atoms:
			ffprint('Number of atoms do not match... fucked up some where')
			sys.exit()
		
		x = 0
		
		traj_list = []
		a = sys[i][1]
		while a <= sys[i][2]:
			traj_list.append('%s%s/Truncated/production.%s/production.%s.dcd' %(traj_loc,sys[i][0],a,a))  
			a += 1
	
		ffprint('Beginning trajectory analysis from system %s' %(sys[i][0]))
		for j in range(len(traj_list)):
			ffprint('Working on Traj %d' %(sys[i][1]+j))
			u.load_new(traj_list[j])

			nSteps = len(u.trajectory)

			for k in range(nSteps):
				if k%(grab_frame) == 0:
					u.trajectory[k]
					ffprint('Writing frame %d to dcd file' %(k))
					u_all.translate(-u_sel.center_of_mass())
					R, rmsd = rotation_matrix(u_align.positions,pos0)
					u_sel.rotate(R)
					W.write(u_sel)
					x += 1
		out1.write('Wrote %d frames for the %s system\n' %(x, sys[i][0]))

W.close()
out1.close()

