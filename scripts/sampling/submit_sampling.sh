#!/bin/bash

N_JOBS=$1
SOURCE_CATEGORY=$2
SOURCE_EXCHANGE=$3

if [ "$#" -eq 4 ]; then
    ALT_C=""
    SUB_DIM=$4

elif [ "$#" -eq 5 ]; then
    ALT_C=$4
    SUB_DIM=$5

else
    echo "Usage:"
    echo "  ./submit_sampling.sh <N_JOBS> <SOURCE_CATEGORY> <SOURCE_EXCHANGE> <SUB_DIM>"
    echo "  ./submit_sampling.sh <N_JOBS> <SOURCE_CATEGORY> <SOURCE_EXCHANGE> <ALT_C> <SUB_DIM>"
    exit 1
fi

if [ "$#" -eq 4 ]; then
    sbatch --array=1-"$N_JOBS" \
        run_sampling.sh \
        "$SOURCE_CATEGORY" "$SOURCE_EXCHANGE" "$SUB_DIM"
else
    sbatch --array=1-"$N_JOBS" \
        run_sampling.sh \
        "$SOURCE_CATEGORY" "$SOURCE_EXCHANGE" "$ALT_C" "$SUB_DIM"
fi
