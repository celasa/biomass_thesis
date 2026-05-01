## Final COBRAme+qMINOS+solveME installation guide

### Requirements
* Anaconda
* qMINOS source code (Michael A. Saunders)
* Download the following file: Makefile_THIS.defs

## Compute following steps inside WSL terminal

**1. Create Anaconda environment**
* conda create --name [env] python=3.6
* conda activate [env]
* pip install git+https://github.com/SBRG/COBRAme.git
* apt -get install gfortran

**2. Compile qMINOS**
* unzip qM.zip (??)
* cd qMINOS/quadLP
* rm Makefile.defs
* cp -f [root_to_file]/Makefile_THIS.defs .
* mv Makefile_THIS.defs Makefile.defs
* cd qMINOS/quadLP/minos56
* make clean
* make
* cd ..
* cd qMINOS/quadLP/qminos56
* make clean
* make
* cd ~

**3. Install and compile solveME**
* git clone https://github.com/SBRG/solvemepy.git
* cd solvemepy
* cp qMINOS/quadLP/minos56/lib/libminos.a ./
* cp qMINOS/quadLP/qminos56/lib/libquadminos.a ./
* python setup.py develop
    
    


