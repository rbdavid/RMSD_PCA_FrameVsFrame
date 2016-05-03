#!/bin/bash 
#SBATCH --job-name=apo.rmsd_pca
#SBATCH --output=apo.traj_rmsd_pca.output 
#SBATCH --time=96:00:00 
#SBATCH --nodes=1
#SBATCH --exclusive 

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/software/usr/gcc-4.9.2/lib64"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/software/usr/hpcx-v1.2.0-292-gcc-MLNX_OFED_LINUX-2.4-1.0.0-redhat6.6/ompi-mellanox-v1.8/lib"

export PYTHON_EGG_CACHE="./"

time ./Traj_writing.py ../../../../../AMBER_apo/truncated.pdb ../../../../../ apo_50framesper.dcd > traj_writing.output

time ./RMSD.all_frames.all_selection.py reference_structure.pdb apo_50framesper.dcd > rmsd_calc.output

time ./PCA.avg_structures.py > pca_calc.output

