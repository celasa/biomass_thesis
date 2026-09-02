#!/bin/bash
#SBATCH --job-name=fba
#SBATCH --output=logs/fba_%A_%a.out
#SBATCH --error=logs/fba_%A_%a.err
#SBATCH --mem=2G
#SBATCH --time=06:00:00

SOLVER=$1
SOURCE=$2
O2=$3

# -------------------------------------
# Select Python environment
# -------------------------------------
if [ "$SOLVER" = "GUROBI" ]; then
    PYTHON="${GUROBI_PYTHON:-$HOME/.conda/envs/cobrame-gurobi/bin/python}"

    # ---------------------------------
    # Check Gurobi license
    # ---------------------------------
    if [ -n "$GRB_LICENSE_FILE" ]; then
        LICENSE_FILE="$GRB_LICENSE_FILE"
    elif [ -f "$HOME/gurobi.lic" ]; then
        LICENSE_FILE="$HOME/gurobi.lic"
    else
        echo "ERROR: No Gurobi license configuration found."
        echo ""
        echo "Set GRB_LICENSE_FILE to your gurobi.lic file, for example:"
        echo "export GRB_LICENSE_FILE=/path/to/gurobi.lic"
        echo ""
        echo "If you have not retrieved/configured your Gurobi license yet,"
        echo "follow the appropriate Gurobi licensing instructions first."
        exit 1
    fi

    export GRB_LICENSE_FILE="$LICENSE_FILE"

elif [ "$SOLVER" = "QMINOS" ]; then
    PYTHON="${QMINOS_PYTHON:-$HOME/.conda/envs/cobrame-qminos/bin/python}"

else
    echo "ERROR: Unknown solver '$SOLVER'"
    echo "Choose GUROBI or QMINOS."
    exit 1
fi

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
"$PYTHON" run_substrate_task.py "$SOLVER" "$SOURCE" "$O2"
