#!/bin/bash
#SBATCH --job-name=fba
#SBATCH --output=logs/fba_%A_%a.out
#SBATCH --error=logs/fba_%A_%a.err
#SBATCH --mem=20G
#SBATCH --time=06:00:00

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

PYTHON="${QMINOS_PYTHON:-$HOME/.conda/envs/cobrame-qminos/bin/python}"

# -------------------------------------
# Check Python environment
# -------------------------------------
if [ ! -x "$PYTHON" ]; then
    echo "ERROR: Python executable not found:"
    echo "$PYTHON"
    exit 1
fi

# -------------------------------------
# Run simulation
# -------------------------------------
if [ "$#" -eq 3 ]; then
    "$PYTHON" solve_sample_point.py \
        "$SOURCE_CATEGORY" "$SOURCE_EXCHANGE" "$SUB_DIM"

else
    "$PYTHON" solve_sample_point.py \
        "$SOURCE_CATEGORY" "$SOURCE_EXCHANGE" "$ALT_C" "$SUB_DIM"
fi
