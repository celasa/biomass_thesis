## Final COBRAme+qMINOS+solveME installation guide

### Requirements
* Anaconda
* qMINOS source code (Michael A. Saunders)
* Download the following file: Makefile_THIS.defs

## Compute following steps inside WSL terminal
1. conda create --name [env] python=3.6
2. conda activate [env]
3. pip install git+https://github.com/SBRG/COBRAme.git
5. apt -get install gfortran
6. unzip qM.zip (??)
7. cd qMINOS/quadLP
8. rm Makefile.defs
9. cp -f [root_to_file]/Makefile_THIS.defs .
10. mv Makefile_THIS.defs Makefile.defs
11. cd qMINOS/quadLP/minos56
12. make clean
13. make
14. cd ..
15. cd qMINOS/quadLP/qminos56
16. make clean
17. make
18. cd ~
19. git clone https://github.com/SBRG/solvemepy.git
20. cd solvemepy
21. cp qMINOS/quadLP/minos56/lib/libminos.a ./
22. cp qMINOS/quadLP/qminos56/lib/libquadminos.a ./
23. python setup.py develop
    
    


