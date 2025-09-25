#!/bin/bash -l

#PBS -N testfile_orca
#PBS -e pbs/test_orca_${PBS_JOBID}.err
#PBS -o pbs/test_orca_${PBS_JOBID}.out
#PBS -l nodes=1:ppn=8
#PBS -l walltime=00:05:00 

# Load environment
source ~/.bashrc
shopt -s expand_aliases
sc
pwd
cd Master_thesis

# Load Python environment
module load vsc-venv
source vsc-venv --activate --requirements requirements.txt --modules modules.txt

# Load ORCA
module load ORCA/6.1.0-gompi-2023b-avx2

# Run the script
#python generate_orca_input.py
python post_process.py
#orca calc.inp > calc.out