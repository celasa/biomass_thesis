# Reproduce the setup for this thesis

Sample space:

1. `conda activate [python environment]`
2. `python generate_sample_space.py <DIMENSION> <SOURCE>`
   
**The uptake range and number of samples is set by default in `generate_sample_space.py` at `max_uptake` and `n_samples`, this can be changed by editing the file from the command line: `nano generate_sample_space.py`**

Sampling procedure:
1. `./submit_sampling.sh <SOURCE_CATEGORY> <SOURCE_EXCHANGE> <SUBSTRATE_DIMENSION>`
2. `./submit_sampling.sh <SOURCE_CATEGORY> <SOURCE_EXCHANGE> <ALT_C_EXCHANGE> <SUBSTRATE_DIMENSION>`
   
**When `<ALT_C_EXCHANGE>` is not specifified, EX_glc__D_e (gucose) is used as default. When `<ALT_C_EXCHANGE>` is provided, an identifier is included in the directory for where the FBA results are stored.**

# LO-sampling

## 1. Generate sample space:
Carbon:
* `python generate_sample_space.py glc_LO`
* `python generate_sample_space.py ac_LO`
* `python generate_sample_space.py lcts_LO`
* `python generate_sample_space.py glyc_LO`
* `python generate_sample_space.py succ_LO`

Nitrogen:
* `python generate_sample_space.py nh4_LO`
* `python generate_sample_space.py arg_LO`
* `python generate_sample_space.py no3_LO`


## 2. Run LO-sampling on the HPC:
Carbon:
* `./submit_sampling.sh C EX_glc__D_e glc_LO`
* `./submit_sampling.sh C EX_ac_e ac_LO`
* `./submit_sampling.sh C EX_lcts_e lcts_LO`
* `./submit_sampling.sh C EX_glyc_e glyc_LO`
* `./submit_sampling.sh C EX_succ_e succ_LO`

Nitrogen:
* `./submit_sampling.sh N EX_nh4_e nh4_LO`
* `./submit_sampling.sh N EX_nh4_e EX_ac_e nh4_LO`

* `./submit_sampling.sh N EX_arg__L_e arg_LO`
* `./submit_sampling.sh N EX_arg__L_e EX_ac_e arg_LO`
* `./submit_sampling.sh N EX_arg__L_e EX_glyc_e arg_LO`

* `./submit_sampling.sh N EX_no3_e no3_LO`
* `./submit_sampling.sh N EX_no3_e EX_glyc_e no3_LO`


# PhPP-sampling

## 1. Gnerate sample space:
Carbon:
* `python generate_sample_space.py glc_PHPP`
* `python generate_sample_space.py ac_PHPP`
* `python generate_sample_space.py lcts_PHPP`
* `python generate_sample_space.py glyc_PHPP`
* `python generate_sample_space.py succ_PHPP`

Nitrogen:
* `python generate_sample_space.py nh4_PHPP`
* `python generate_sample_space.py arg_PHPP`
* `python generate_sample_space.py no3_PHPP`


## 2. Run PHPP-sampling on the HPC:
Carbon:
* `./submit_sampling.sh C EX_glc__D_e glc_PHPP`
* `./submit_sampling.sh C EX_ac_e ac_PHPP`
* `./submit_sampling.sh C EX_lcts_e lcts_PHPP`
* `./submit_sampling.sh C EX_glyc_e glyc_PHPP`
* `./submit_sampling.sh C EX_succ_e succ_PHPP`

Nitrogen:
* `./submit_sampling.sh N EX_nh4_e nh4_PHPP` 
* `./submit_sampling.sh N EX_nh4_e EX_ac_e nh4_PHPP` 

* `./submit_sampling.sh N EX_arg__L_e arg_PHPP`
* `./submit_sampling.sh N EX_arg__L_e EX_ac_e arg_PHPP`
* `./submit_sampling.sh N EX_arg__L_e EX_glyc_e arg_PHPP`

* `./submit_sampling.sh N EX_no3_e nh4_PHPP`
* `./submit_sampling.sh N EX_no3_e EX_glyc_e nh4_PHPP`
