import numpy as np
import warnings

# -----------------------------
# Suppress the lxml SBML warning
# -----------------------------
warnings.filterwarnings(
    "ignore",
    message=".*",
    category=UserWarning
)

from lhs import generate_sample_space

# -----------------------------
# Input args
# -----------------------------
LO = $1 
RANGE = $2
N_SAMPLES = $3

sample = generate_sample_space(source_range=RANGE, oxygen_range=RANGE, lo=LO, n_samples=N_SAMPLES)
np.save(f"sample_space.npy", sample)
