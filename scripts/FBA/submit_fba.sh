#!/bin/bash

SOLVER=$1
SOURCE=$2
O2=$3

N_TASKS=$(python -c "
import pickle
import fba_scripts

with open('../../files/iJL1678b.pickle', 'rb') as f:
    me = pickle.load(f)

source = '$SOURCE'
types = ['C', 'N', 'P', 'S'] if source == 'ALL' else [source]

print(sum(len(fba_scripts.get_source_list(me, s)) for s in types))
")

sbatch --array=1-"$N_TASKS" run_fba.sh "$SOLVER" "$SOURCE" "$O2"
