# Reproduce the setup for this thesis

1. `./submit_sampling.sh <SOURCE_CATEGORY> <SOURCE_EXCHANGE> <SUBSTRATE_DIMENSION>`
2. `./submit_sampling.sh <SOURCE_CATEGORY> <SOURCE_EXCHANGE> <ALT_C_EXCHANGE> <SUBSTRATE_DIMENSION>`

# LO-sampling
* DIMENSION = LO

## 1. Generate sample space:


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

* `./submit_sampling.sh N EX_no3_e nh4_LO`
* `./submit_sampling.sh N EX_no3_e EX_glyc_e nh4_LO`


# PhPP-sampling

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
