# Engineering Physics & Industry: Activated_Carbon

## Setting up hpc with VS Code

### 1. Generate ssh keys for accessing hpc
follow instructions here:
https://docs.hpc.ugent.be/Linux/account/

Make a separate "hpc" directory in .ssh and store the ssh keys there.

### 2. Add ssh key to ssh-agent

### 3. Add to SSH config

change `vsc48514` with your username:

```
Host hpc
    HostName login.hpc.ugent.be
    User vsc48514
    ForwardAgent yes
    ForwardX11 yes

Match User vsc48514
    IdentityFile ~/.ssh/hpc/id_rsa_vsc
```

### 4. Upload public (.pub) SSH key to VSC accountpage

### 5. Check login via terminal:
Always use eduroam or ugent's vpn when using the hpc!

In terminal:
```
ssh vsc48514@login.hpc.ugent.be
```

## Using hpc with VS Code

-Install the `Remote - SSH` VS Code extension.

When connecting:                            <br>
-Open search bar (at the top) of VS Code    <br>
-Click on `Show and Run Commands`           <br>
-Type: `Remote-SSH: Connect To Host`        <br>
-Select `hpc`                               <br>

You should now be connected to the hpc, via VS Code!

## Add github repository to hpc

Make sure you're connected to the hpc (in terminal or via VS Code). <br>
If you're connected via VS Code, you should use the VS Code terminal for all commands on the hpc!   <br>

Check current working directory:
```
pwd
```
You should be at your home directory: e.g. `/user/gent/485/vsc48514/`     <br>
If not, move there  (via `cd` in terminal).

On this homepage you should see a `.ssh` directory.

### Setup github via ssh
Now you need to setup github on the hpc (remember, the hpc runs on Linux!), as you would do on your normal computer. <br>
(Check the tutorial here if you forgot: https://ugent-visualisations-maths-and-physics.github.io/setup_support.html)  <br>   
So generate ssh keys in the `.ssh` directory of your home directory on the hpc, add them to your github.com account and you should be able to connect to github (check this before moving to the next section!)

### Setup .bashrc file
On your home directory on the hpc, you should also find a `.bashrc` file.      <br>
Add following lines at the end of the `.bashrc` file (are aliases for commands which are commonly used):

```
# custom .bashrc lines
# locate powerbash: 
source ~/.local/bin/powerbash.sh

# aliases for moving to clusters
alias j='module swap cluster/joltik'
alias d='module swap cluster/doduo'
alias a='module swap cluster/accelgor'
alias n='module swap cluster/donphan'
alias g='module swap cluster/gallade'
alias s='module swap cluster/shinx'

# aliases for quee job
alias qa='squeue --cluster=ALL'
alias w='watch -n2 squeue -l'
# move to data or scratch repository
alias da="cd ${VSC_DATA}"
alias sc="cd ${VSC_SCRATCH}"

# Aliases for interactive jobs (3 hours here). Don't use these for production (=super long) computations.
for num in $(seq 1 36); do 
  alias work${num}="srun --pty -t 3:00:00 --nodes=1 --ntasks=1 --cpus-per-task=${num} --mem=10G bash"
done
```

### Clone repository from github to scratch directory on hpc
Never store code (.py) files on the home directory. <br>
Code should be stored in the scratch directory (e.g. `/scratch/gent/485/vsc48514/`)  <br>
So move to that directory via terminal (one of the aliases of the previous section is used here).  <br>
In terminal:
```
sc
```

Now clone the git repository (via its URL) here.
In terminal:
```
git clone https://github.com/Simon-Verbruggen/EPI_Activated_Carbon.git
```
The repository should now be cloned and visible, move to it via cd, in terminal:
```
cd EPI_Activated_Carbon
```
Now, this repository should be recognised by VS Code, and you can push, pull...as in a normal repository. Anyway, you can still also do this via terminal.

### Install powerbash on hpc (optional, I think)
In terminal:
```
mkdir -p ~/.local/bin
curl -Ls https://raw.githubusercontent.com/napalm255/powerbash/master/powerbash.sh -o ~/.local/bin/powerbash.sh
```
## Setup virtual environment on hpc
Link to documentation:                                                      <br>
https://docs.hpc.ugent.be/Linux/setting_up_python_virtual_environments/     <br>
Specifically we just need to do this (line per line in terminal):

```
n
qsub -I
sc
cd EPI_Activated_Carbon
module load vsc-venv
source vsc-venv --activate --requirements requirements.txt --modules modules.txt
```

`modules.txt`: modules loaded before creating virtual environment                                 <br>
`requirements.txt`: libraries (pip install) which are installed in the virtual environment        <br>

This virtual environment is cluster specific. The first time this is ran on a cluster, the requirements are installed.  
The next times, the virtual environment is still there and is just activated.

Explanation of code (line by line):                                                                 <br>
Go to `donphan` cluster (is meant for interactive jobs and has GPU support)                         <br>
Start interactive job.                                                                              <br>
Move to sratch directory.                                                                           <br>
Move to repository.                                                                                 <br>
Load module for creating virtual environments on hpc and create virtual environment                  <br>

## Use hpc

Activate the virtual environment: exactly the same steps as in `Setup virtual environment on hpc`

### Run a python file

Files can now be run, by for example:
```
python activated_coal_hpc.py
```
The plot outputs of this particular file are written to a directory `output_hpc` which should become visible 1 minute max after running.  <br>

## Batch jobs
We need GPU support, the GPU clusters are `joltik`, `accelgor` and `littleo` (new).  <br>
Make sure to specify 12 supporting CPU's per GPU on `accelgor` and 8 supporting CPU's per GPU on `joltik` (specify this in the .pbs file, below).
First navigate to a cluster, for example for accelgor (in terminal):
```
a
```
You can always check availability of clusters via https://login.hpc.ugent.be/pun/sys/dashboard/

Make sure to put a .pbs file in the EPI_Activated_Carbon directory.   <br>
An example .pbs file is given here (this is called `activated_coal_hpc.pbs`).   <br>
Change the email adress!!

```
#!/bin/bash -l

#PBS -N activated_carbon
#PBS -e pbs/activated_carbon_${PBS_JOBID}.err
#PBS -o pbs/activated_carbon_${PBS_JOBID}.out
#PBS -m abe
#PBS -M <email>
#PBS -l nodes=1:ppn=8:gpus=1,mem=32gb
#PBS -l walltime=0:45:00

source ~/.bashrc
shopt -s expand_aliases
sc
pwd
cd EPI_Activated_Carbon
module load vsc-venv
source vsc-venv --activate --requirements requirements.txt --modules modules.txt

python activated_carbon_NVT.py
```

To submit job type (in terminal):
```
qsub activated_carbon.pbs
```

For debugging on these clusters,  an interactive session can be started:
```
qsub -I -l walltime=0:10:00 -l nodes=1:ppn=4:gpus=1,mem=16gb
```

Look for output files: `.out` and error files: `.err`

## loop the pbs
edit your pbs files accordingly. You should edit to the right python file. YOU SHOULD HAVE A DIFFERENT PBS FILE FOR NPT AND NVT. THEY SHOULD BE NAMED "PBS_NPT.pbs" and "PBS_NVT.pbs" SINCE THOSE ARE CALLED IN THE SH CODES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

``` 
#!/bin/bash -l

#PBS -N activated_carbon
#PBS -e pbs/activated_carbon_${PBS_JOBID}.err
#PBS -o pbs/activated_carbon_${PBS_JOBID}.out
#PBS -m abe
#PBS -M <email>
#PBS -l nodes=1:ppn=8:gpus=1,mem=32gb
#PBS -l walltime=00:10:00

source ~/.bashrc
shopt -s expand_aliases
sc
pwd
cd EPI_Activated_Carbon
module load vsc-venv
source vsc-venv --activate --requirements requirements.txt --modules modules.txt


# Read environment variables (set in qsub command)
TEMP=$PBS_TEMP
STEPS=$PBS_STEPS
MOLECULES=$PBS_MOLECULES
DENSITY=$PBS_DENSITY
FOLDER=$PBS_FOLDER

# Run the Python script with these variables
python activated_carbon_NVT.py --temperature "$TEMP" --steps "$STEPS" --molecules "$MOLECULES" --density "$DENSITY" --folder "$FOLDER"
```

Next you create .sh files (for both NVT and NPT), they should be called "submit_jobs_NVT.sh" and "submit_jobs_NPT.sh"

copy this in the files (change for NPT accordingly, there are multiple NVT's that should be changed to NPT(_MTK)!!!)

Add the files to .gitignore

```
#!/bin/bash

# Define parameter ranges, spaces inbetween different options!
temperatures=(600 900 1200)
steps=(10000)       
molecules=(10 100 300) 
densities=(1 2 3)        
folders=("all") #all, none or O2H2, in strings!

# Loop through all combinations
for folder in "${folders[@]}"; do
  for temp in "${temperatures[@]}"; do
      for step in "${steps[@]}"; do
          for mol in "${molecules[@]}"; do
              for dens in "${densities[@]}"; do
                  JOB_NAME="NVT_NPC-${dens}_${folder}_${mol}_${temp}K"
                  echo "Submitting job: Temp=$temp, Steps=$step, Molecules=$mol, Density=$dens, Folder = $folder"
                  qsub -N "$JOB_NAME" \
                      -v PBS_TEMP="$temp",PBS_STEPS="$step",PBS_MOLECULES="$mol",PBS_DENSITY="$dens",PBS_FOLDER="$folder" \
                      PBS_NVT.pbs
              done
          done
      done
  done
done
```

```
j
sc
cd EPI_Activated_Carbon
chmod +x submit_jobs_NVT.sh #this line only the first time
./submit_jobs_NVT.sh
```


## dependencies

ORB:
pip install orb-models

py3Dmol:
pip install py3Dmol

pynanoflann:
pip install pynanoflann
