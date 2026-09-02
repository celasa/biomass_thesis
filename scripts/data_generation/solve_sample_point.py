import os
import sys
import numpy as np
import pandas as pd
import warnings
from pathlib import Path

from lhs import load_me, run_phpp_sampler

# -----------------------------
# Suppress the lxml SBML warning
# -----------------------------
warnings.filterwarnings(
    "ignore",
    message="Install lxml for faster SBML I/O",
    category=UserWarning
)

# ==============================
# Input arguments
# ==============================
if len(sys.argv) not in {4, 5}:
    sys.exit(
        "Usage:\n"
        "  python run_sampling.py <SOURCE_CATEGORY> <SOURCE_EXCHANGE> <SUBSTRATE_DIMENSION>\n"
        "or\n"
        "  python run_sampling.py <SOURCE_CATEGORY> <SOURCE_EXCHANGE> <ALT_C_EXCHANGE> <SUBSTRATE_DIMENSION>"
    )

source_category = sys.argv[1].upper() #C or N
source_exchange = sys.argv[2] # Exchange reaction for C or N source

if len(sys.argv) == 5:
  alt_C = sys.argv[3] #Exchange for alternative C-source
  sub_dim = sys.argv[4] # for instance: glc_PHPP
else:
  alt_C = None
  sub_dim = sys.argv[3]

substrate, dimension = sub_dim.split("_")[:2]
dimension = dimension.upper() 

# -------------------------------------
# File paths
# -------------------------------------
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
FILES = ROOT / "files"

SAMPLE_DIR = DATA / "sample_spaces" / dimension 

model_path = FILES / "iJL1678b.pickle"
lhs_file = SAMPLE_DIR / f"{substrate}_{dimension}_sample_space.npy"

output_dir = DATA / dimension / substrate
output_dir.mkdir(parents=True, exist_ok=True)

flux_dir = output_dir / "flux"
shadow_dir = output_dir / "shadow"

flux_dir.mkdir(parents=True, exist_ok=True)
shadow_dir.mkdir(parents=True, exist_ok=True)

if not lhs_file.exists():
    sys.exit(
        f"Sample-space file not found:\n{lhs_file}\n"
        "Generate the sample space before submitting this job."
    )

# -----------------------------
# Load samples
# -----------------------------
all_samples = np.load(lhs_file, allow_pickle=True)

if all_samples.ndim == 1:
    # Legacy / genuinely 1D array
    samples = [(s,) for s in all_samples]

elif all_samples.ndim == 2:
    # Current LO (N x 1) or PHPP (N x 2) format
    samples = [tuple(s) for s in all_samples]

else:
    sys.exit(
        f"Unexpected sample-space shape: {all_samples.shape}"
    )

# ==============================
# 2. Split samples for array jobs
# ==============================
task_id = int(os.environ["SLURM_ARRAY_TASK_ID"]) - 1
n_jobs = int(os.environ["SLURM_ARRAY_TASK_COUNT"])

chunks = np.array_split(samples, n_jobs)
my_chunk = chunks[task_id]

if task_id < 0 or task_id >= len(chunks):
    sys.exit(
        f"SLURM task ID {task_id + 1} is outside the valid range "
        f"1-{len(chunks)}."
    )

# ==============================
# 3. Run samples with timeout & crash handling
# ==============================
start_idx = sum(len(chunks[i]) for i in range(task_id))

if dimension == "LO":
    lo_fixed = -1000
elif dimension == "PHPP":
    lo_fixed = None
else:
    sys.exit(
        f"Unknown dimension '{dimension}'. "
        "Choose LO or PHPP."
    )

for local_idx, sample_point in enumerate(my_chunk):
    model = load_me(model_path)
    sample_idx = start_idx + local_idx  

    try:
        phenotype = run_phpp_sampler(model=model, source_category=source_category, source=source_exchange, sample_point=sample_point, lo_fixed=lo_fixed, alt_C=alt_C)
  
        # Save fluxes
        flux_df = pd.DataFrame(list(model.solution.x_dict.items()), columns=["reaction", "flux"])
        flux_path = flux_dir / f"flux_task{task_id + 1}_sample{sample_idx}.pkl"
        flux_df.to_pickle(flux_path)

        # Save shadow prices
        shadow_df = pd.DataFrame(list(model.solution.y_dict.items()), columns=["metabolite", "shadow_price"])
        shadow_path = shadow_dir / f"shadow_task{task_id + 1}_sample{sample_idx}.pkl"
        shadow_df.to_pickle(shadow_path)


    except Exception as e:
        print(f"Sample {sample_idx} failed due to: {e}. Skipping...")
        continue

