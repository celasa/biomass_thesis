## Final COBRAme+qMINOS+solveME installation guide

Here are all the necessary steps to create a Python environment to solve ME-models using qMINOS. All the steps from the start are provided first,
but if it is necessary to create a new conda environment with qMINOS and solveME previously compiled go to the second section:

### Requirements
* Anaconda
* qMINOS source code (Michael A. Saunders)
* Download the following file: Makefile_THIS.defs into [root_directory] directory



## Compute following steps inside WSL terminal

**1. Create Anaconda environment**
[root_directory]
* conda create --name [env] python=3.6
* conda activate [env]
* pip install git+https://github.com/SBRG/COBRAme.git
* apt -get install gfortran

**2. Compile qMINOS**
[root_directory]
* cd qMINOS
    * unzip qM.zip (??)
    * cd qMINOS/quadLP
        * rm Makefile.defs
        * cp -f [root_directory]/Makefile_THIS.defs .
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
[root_directory]
* git clone https://github.com/SBRG/solvemepy.git
* cd solvemepy
  * cp qMINOS/quadLP/minos56/lib/libminos.a ./
    * cp qMINOS/quadLP/qminos56/lib/libquadminos.a ./
        * cd ..
    * python setup.py develop
    
## If the above steps have been completed before, create a new Conda environment like this:
Create conda environment
[root_directory]
1. conda create --name [NAME_ENV] python=3.6
2. conda activate [NAME_ENV]
3. cd solvemepy
   * python setup.py develop


