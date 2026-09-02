import sys
import os
import pickle
import pandas as pd
from pathlib import Path

import fba_scripts

# -------------------------------------
# Input args
# -------------------------------------
if len(sys.argv) != 4:
    sys.exit(
        "Usage: python run_substrate_task.py "
        "<SOLVER> <SOURCE_TYPE> <O2_FLAG>"
    )

solver = sys.argv[1].upper()
source_arg = sys.argv[2].upper()

if sys.argv[3] not in {"0", "1"}:
    sys.exit("O2_FLAG must be 0 or 1.")

o2_on_off = sys.argv[3] == "1"

valid_sources = ["C", "N", "P", "S"]

if source_arg == "ALL":
    source_types = valid_sources
elif source_arg in valid_sources:
    source_types = [source_arg]
else:
    sys.exit(
        f"Unknown source type '{source_arg}'. "
        "Choose C, N, P, S, or ALL."
    )

# -------------------------------------
# File paths
# -------------------------------------
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
FILES = ROOT / "files"

sys.path.append(str(ROOT))

model_path = FILES / "iJL1678b.pickle"

output_dir = DATA / f"{solver.lower()}_results"
output_dir.mkdir(parents=True, exist_ok=True)

failed_log_file = output_dir / f"failed_runs_{source_type}.csv"

# -------------------------------------
# Load model
# -------------------------------------
with open(model_path, "rb") as f:
    me = pickle.load(f)

# -------------------------------------
# Build task list
# -------------------------------------
tasks = []

for source_type in source_types:
    substrates = fba_scripts.get_source_list(me, source_type)

    for substrate in substrates:
        tasks.append((source_type, substrate))     
# -------------------------------------
# Select current SLURM task
# -------------------------------------
task_id = int(os.environ["SLURM_ARRAY_TASK_ID"]) - 1

if task_id < 0 or task_id >= len(tasks):
    sys.exit(
        f"Task ID {task_id + 1} out of range. "
        f"{source_arg} contains {len(tasks)} tasks."
    )

source_type, input_substrate = tasks[task_id]
# -------------------------------------
# Select solver
# -------------------------------------
if solver == "GUROBI":
    from gurobi_utils import run_substrate
elif solver == "QMINOS":
    from qminos_utils import run_substrate

else:
    sys.exit(
        f"Unknown solver '{solver}'. "
        "Choose GUROBI or QMINOS."
    )

# -------------------------------------
# Set environment
# -------------------------------------
fba_scripts.set_env(
    model=me,
    aerobic=o2_on_off,
    source=source_type,
)
condition = "aerobic" if o2_on_off else "anaerobic"

# -------------------------------------
# Solve model
# -------------------------------------
result = None

try:
    result = run_substrate(
        model=me,
        substrate=input_substrate,
    )

except Exception as e:
    print(
        f"[ERROR] {solver} failed for "
        f"{input_substrate}: {e}"
    )

    with open(failed_log_file, "a", newline="") as f:
        f.write(
            f"{input_substrate},"
            f"{source_type},"
            f"{condition},"
            f"{task_id + 1},"
            f"{solver}\n"
        )
        f.flush()


# -------------------------------------
# Save results
# -------------------------------------
if result is not None:

    flux_path = (
        output_dir
        / f"flux_{input_substrate}_{source_type}_{condition}.csv"
    )

    pd.DataFrame(
        list(result["fluxes"].items()),
        columns=["reaction", "flux"],
    ).to_csv(flux_path, index=False)

    shadow_path = (
        output_dir
        / f"shadow_{input_substrate}_{source_type}_{condition}.csv"
    )

    pd.DataFrame(
        list(result["shadow"].items()),
        columns=["metabolite", "shadow_price"],
    ).to_csv(shadow_path, index=False)
