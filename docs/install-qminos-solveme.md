
## 1. Obtain the qMINOS Source code from Michael A. Saundersat Standford University, and unzip the files in home directiory (root)

## 2. Compile qMINOS in home directory (root)

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

## 3. Install and compile solveME in home directory (root)
```bash
[root] git clone https://github.com/SBRG/solvemepy.git
[root] cd solvemepy
[root/solvemepy] cp qMINOS/quadLP/minos56/lib/libminos.a ./
[root/solvemepy] cp qMINOS/quadLP/qminos56/lib/libquadminos.a ./
[root/solvemepy] python setup.py develop
```

## 4. Create conda environment with qMINOS:
```bash
[root] conda env create -f requirements/cobrame-qminos.yml -n cobrame-qminos
```
