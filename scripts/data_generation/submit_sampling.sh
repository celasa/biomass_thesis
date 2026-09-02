#!/bin/bash

SOURCE_CATEGORY=$1
SOURCE_EXCHANGE=$2

if [ "$#" -eq 3 ]; then
    ALT_C=""
    SUB_DIM=$3

elif [ "$#" -eq 4 ]; then
    ALT_C=$3
    SUB_DIM=$4

else
    echo "Error: expected 3 or 4 arguments."
    exit 1
fi

N_JOBS=20

if [ "$#" -eq 3 ]; then
    sbatch --array=1-"$N_JOBS" \
        run_sampling.sh \
        "$SOURCE_CATEGORY" "$SOURCE_EXCHANGE" "$SUB_DIM"
else
    sbatch --array=1-"$N_JOBS" \
        run_sampling.sh \
        "$SOURCE_CATEGORY" "$SOURCE_EXCHANGE" "$ALT_C" "$SUB_DIM"
fi
