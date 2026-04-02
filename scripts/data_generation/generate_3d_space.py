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

from lhs import generate_3d_sample_space

c1_source = 'EX_glc__D_e'
c2_source = 'EX_ac_e'
n_samples = 1000
c1_range = (-120.0, 0.0)
c2_range = (-130.0, 0.0)

sample = generate_3d_sample_space(c1_range=c1_range, c2_range=c2_range, oxygen_range=None, po=True, n_samples=n_samples, criterion='maximin')
np.save("LHS_glc_ac_samples.npy", sample)
