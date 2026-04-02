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

c_source = 'EX_nh4_e'
n_samples = 700
c_range = (-135.0, 0.0)
o_range= (-135.0, 0.0)

sample = generate_sample_space(carbon_range=c_range, oxygen_range=o_range, lo=False, n_samples=n_samples)
np.save(f"LHS_nh4_ac_samples.npy", sample)
