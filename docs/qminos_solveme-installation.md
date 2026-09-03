# Alternative to the official installation instructions of qMINOS

Here are the necessary steps for the alternative installation guide to create a Python environment to solve ME-models using qMINOS and solveME. The official downloading instructions are provided with the qMINOS source code and at the Github repositories for COBRAme and solveME:
* COBRAme: https://github.com/sbrg/cobrame?tab=readme-ov-file
* solveME: https://github.com/SBRG/solvemepy/tree/master

### Requirements
* Anaconda
* qMINOS source code (Michael A. Saunders), download and unzip the files inside the [root] directory
* Download the following file from this repository: `files/Makefile.defs.txt` into [root] directory where you will be compiling qMINOS

## 1. Compile qMINOS in home directory (root)
**After unzipping the files**

```bash
[root] cd qMINOS
[root/qMINOS] cd qMINOS/quadLP
[root/qMINOS/quadLP] rm Makefile.defs
[root/qMINOS/quadLP] cp -f biomass_thesis/files/Makefiles.defs.txt .
[root/qMINOS/quadLP] mv Makefile.defs.txt Makefile.defs
[root/qMINOS/quadLP] cd qMINOS/quadLP/minos56
[root/qMINOS/quadLP/minos56] make clean
[root/qMINOS/quadLP/minos56] make
[root/qMINOS/quadLP/minos56] cd ..
[root/qMINOS/quadLP] cd qMINOS/quadLP/qminos56
[root/qMINOS/quadLP/qminos56] make clean
[root/qMINOS/quadLP/qminos56] make
[root/qMINOS/quadLP/qminos56] cd ~
```

## 2. Install and compile solveME in home directory (root)
```bash
[root] git clone https://github.com/SBRG/solvemepy.git
[root] cd solvemepy
[root/solvemepy] cp qMINOS/quadLP/minos56/lib/libminos.a ./
[root/solvemepy] cp qMINOS/quadLP/qminos56/lib/libquadminos.a ./
[root/solvemepy] python setup.py develop
```

## 3. Create conda environment with qMINOS:
```bash
[root] conda env create -f requirements/cobrame-qminos.yml -n cobrame-qminos
```



