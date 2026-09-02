import numpy as np
import warnings
import sys
from pathlib import Path

from lhs import generate_sample_space

# -----------------------------
# Suppress the lxml SBML warning
# -----------------------------
warnings.filterwarnings(
    "ignore",
    message=".*",
    category=UserWarning
)


# -----------------------------
# Input args
# -----------------------------
if len(sys.argv) != 5:
    sys.exit(
        "Usage: python generate_sample_space.py "
        "<DIMENSION> <SOURCE>"
    )

dimension = sys.argv[1].upper()
max_uptake = -200.0  # EDIT TO CHANGE MAX POSSIBLE UPTAKE
n_samples = 1000 # EDIT TO CHANGE NUMBER OF SAMPLE POINTS TO GENERATE
source = sys.argv[4].upper()


# -----------------------------
# Validate dimension
# -----------------------------
if dimension == "LO":
    lo = True
elif dimension == "PHPP":
    lo = False
else:
    sys.exit("DIMENSION must be LO or PHPP.")
    
# -----------------------------
# Sample space settings
# -----------------------------
uptake_range = (max_uptake, 0.0)

sample = generate_sample_space(
    source_range=uptake_range,
    oxygen_range=uptake_range,
    lo=lo,
    n_samples=n_samples,
)

# -----------------------------
# Output directory
# -----------------------------
ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DIR = ROOT / "data" / "sample_spaces" / dimension

SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Save sample space
# -----------------------------
sample_path = SAMPLE_DIR / f"{source}_{dimension}_sample_space.npy"

np.save(sample_path, sample)

print(f"Saved sample space to: {sample_path}")
