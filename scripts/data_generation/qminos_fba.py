import fba_scripts
from qminos_utils import run_substrate_qminos
import sys
import os
import pickle
import pandas as pd
import csv
from pathlib import Path

# -------------------------------------
# Input args
# -------------------------------------
if len(sys.argv) != 3:
    sys.exit("Usage: python run_substrate_task.py <SOURCE_TYPE> <O2_FLAG>")

source_type = sys.argv[1]           # 'C', 'N', 'P', or 'S'
o2_on_off = bool(int(sys.argv[2]))    # 1=True, 0=False

# SLURM task index
task_id = int(os.environ['SLURM_ARRAY_TASK_ID']) - 1  # SLURM_ARRAY_TASK_ID (starts at 1)

# -------------------------------------
# File paths
# -------------------------------------
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
FILES = ROOT / "files"

sys.path.append(str(ROOT))

model_path = FILES / "iJL1678b.pickle"
output_dir = DATA / "qminos_results"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Failed substrates log file
failed_log_file = os.path.join(output_dir, f"failed_runs_{source_type}.csv")

# -------------------------------------
# Load model
# -------------------------------------
with open(model_path, 'rb') as f:
    me = pickle.load(f)

# -------------------------------------
# Allocate substrates to each jobARRAY task
# -------------------------------------
substrates = fba_scripts.get_source_list(me, source_type)

if task_id <0 or task_id >= len(substrates):
    sys.exit(f"Task ID {task_id+1} out of range for {source_type} list")

input_substrate = substrates[task_id]

# -------------------------------------
# Set envrionment
# -------------------------------------
fba_scripts.set_env(model=me, aerobic=o2_on_off, source=source_type)
condition = "aerobic" if o2_on_off else "anaerobic"

# -------------------------------------
# Solve model
# -------------------------------------
result = None
try:
    result = run_substrate_qminos(model=me, substrate=input_substrate)
except Exception as e:
    print(f"[ERROR] Failed for {input_substrate}: {e}")
    failed_log_file = os.path.join(output_dir, f"failed_runs_{source_type}.csv")
    with open(failed_log_file, "a", newline="") as f:
        f.write(f"{input_substrate},{source_type},{condition},{task_id}\n")
        f.flush()

# -------------------------------------
# Saving results to file
# -------------------------------------
if result is not None:
    # Flux file
    flux_path = os.path.join(output_dir, f"flux_{input_substrate}_{source_type}_{condition}.csv")
    pd.DataFrame(list(result["fluxes"].items()), columns=["reaction", "flux"]).to_csv(flux_path, index=False)

    # Shadow price file
    shadow_path = os.path.join(output_dir, f"shadow_{input_substrate}_{source_type}_{condition}.csv")
    pd.DataFrame(list(result["shadow"].items()), columns=["metabolite", "shadow_price"]).to_csv(shadow_path, index=False)
