# Studying the Transformation of Nutritional Input into Macromolecular Biomass Composition in iJL1678b-ME

This project investigates how the biomass composition predicted by the metabolic and gene expression (ME-) model of *Escherichia Coli*, iJL1678b-ME, depends on the *in silico* growth conditions. The project is divided into three parts: (1) solver selection, (2) sampling of the line of optimality (LO) and latin hypercube sampling (LHS) of the phenotype phaseplane (PhPP), and (3) machine learning (ML) to predict the growth condition from the biomass composition. The pipelines that were developed for these respective parts are provided in the repository.

## Repository structure 
```text
.
├── data                                
│   ├── biomass_datasets
│   ├── ml_data
│   └── results
├── docs
│   ├── cobrame-installation.md
│   ├── datasets-construction.md
│   └── qminos_solveme-installation.md
├── files
│   ├── bm_rxns_template.csv
│   ├── iJL1678b.pickle
│   ├── iJL1678b.zip
│   └── macro_template.csv
├── .gitignore
├── notebooks
│   ├── classifier_experiments.ipynb
│   ├── EDA.ipynb
│   ├── gurobi_feasibility.ipynb
│   ├── make_datasets.ipynb
│   ├── make_pickle.ipynb
│   └── tuning.ipynb
├── README.md
├── requirements
│   ├── analysis-ml.yml
│   ├── cobrame-gurobi.yml
│   └── cobrame-qminos.yml
└── scripts
    ├── EDA
    ├── FBA
    ├── ML
    ├── sampling
    └── solver_selection
```
1. `data/` — input datasets, generated sample spaces, and simulation outputs.
2. `files/` — ME-model and supporting files required by the simulation pipelines.
3. `requirements/` — Conda environment specifications.
4. `scripts/FBA/` — scripts for substrate-specific FBA simulations using Gurobi or qMINOS.
5. `scripts/sampling/` — scripts for generating PhPP and LO data.


## Installation

Clone the repository:

```bash
git clone <repository-url>
cd biomass_thesis
```

### Conda environments

Separate Conda environments are provided for the solver configurations and downstream analyses.

#### Gurobi

```bash
conda env create -f requirements/gurobi.yml -n cobrame-gurobi
```

#### qMINOS

See the qMINOS solver requirements below before creating this environment.

#### Machine learning and exploratory data analysis

```bash
conda env create -f requirements/analysis-ml.yml -n analysis-ml
```

### Solver requirements

#### Gurobi

Gurobi simulations require a valid Gurobi license in addition to the `cobrame-gurobi` Conda environment. The license must be configured on the system where the simulations are run. A free academic license can be obtained from the [Gurobi Academic Program](https://www.gurobi.com/academics/).

#### qMINOS

qMINOS simulations require installations of both **qMINOS** and **solvemepy**. These must be installed and configured before running the qMINOS simulation pipeline.

qMINOS is not distributed with this repository and requires access to the qMINOS source code, which can be obtained from Prof. Michael A. Saunders at Stanford University. Detailed instructions for obtaining, installing, and configuring qMINOS and solvemepy are provided in [`docs/qminos_solveme-installation.md`](docs/qminos_solveme-installation.md).

Once qMINOS and solvemepy are installed, create the corresponding Conda environment:

```bash
conda env create -f requirements/cobrame-qminos.yml -n cobrame-qminos
```

## FBA simulations
The FBA pipeline evaluates individual nutrient sources using either **Gurobi** or **QMINOS**.

Submit simulations from `scripts/FBA/`:

```bash
cd scripts/FBA
./submit_fba.sh <SOLVER> <SOURCE> <O2>
```

Arguments:

- `<SOLVER>` — `GUROBI` or `QMINOS`
- `<SOURCE>` — `C`, `N`, `P`, `S`, or `ALL`
- `<O2>` — `1` for aerobic conditions or `0` for anaerobic conditions

For example:

```bash
./submit_fba.sh GUROBI C 1
```

runs aerobic carbon-source simulations using Gurobi.

`submit_fba.sh` determines the number of substrates and submits the corresponding SLURM array. Each array task evaluates one substrate.

Results are written to:

```text
data/gurobi_results/
data/qminos_results/
```
> **Note:** The FBA simulation pipeline in this repository was refactored from code developed for the study *Computation of condition-dependent proteome allocation reveals variability in the macro and micro nutrient requirements for growth* by Lloyd et al. (2021). The implementation has been reorganized and modified for the simulation workflows used in this project.

## Sampling the line of optimality (LO) and the phenotype phaseplane (PhPP)

The sampling pipeline consists of two steps:

1. Generate a Latin hypercube sample space.
2. Solve the sampled conditions using a SLURM array.

Two sampling modes are supported. The `<DIMENSION>` argument specifies the sampling mode and must be either `PHPP` or `LO`::

- `PHPP` — two-dimensional sampling of substrate and oxygen uptake across the phenotype phaseplane (PhPP sampling).
- `LO` — one-dimensional sampling of substrate uptake across the line of optimality (LO sampling).

### 1. Generate a sample space

From `scripts/sampling/`:

```bash
python generate_sample_space.py <DIMENSION> <SOURCE>
```

For example:

```bash
python generate_sample_space.py PHPP glc
```

Generated sample spaces are stored under:

```text
data/sample_spaces/
```
* The above example is saved as `glc_PHPP_sample_space.npy` file under `data/sample_spaces/PHPP`

### 2. Submit sampling jobs

Without an alternative carbon source (e.g. glucose is used as carbon source):

```bash
./submit_sampling.sh <N_JOBS> <SOURCE_CATEGORY> <SOURCE_EXCHANGE> <SOURCE_DIMENSION>
```
Dimension refer to LO (1D) or PHPP (2D)

For example:

```bash
./submit_sampling.sh 400 C EX_glc__D_e glc_PHPP
```

With an alternative carbon source for nitrogen PhPP:

```bash
./submit_sampling.sh <N_JOBS> <SOURCE_CATEGORY> <SOURCE_EXCHANGE> <ALT_C_EXCHANGE> <SOURCE_DIMENSION>
```

For example:

```bash
./submit_sampling.sh 400 N EX_nh4_e EX_ac_e nh4_PHPP
```

`N_JOBS` specifies the number of SLURM array tasks. The generated sample space is divided between these tasks, and each task solves its assigned sample points sequentially.

Sampling results are written to:

```text
data/PHPP_samples/
data/LO_samples/
```
In the example with glucose:
* 400 of the sample points in `glc_PHPP_sample_space.npy` in parallell, and each feasible FBA result is stored under `data/PHPP_samples/glc`
* Flux vectors are stored in `data/PHPP_samples/glc/flux`
* Shadow prices are stored in `data/PHPP_samples/glc/shadow`

The results from the ammonium environment with acetate as carbon source, the results are stored in:
* `data/PHPP_samples/nh4_ac`

## Data

Some datasets required by the analysis may be distributed as compressed archives because individual files exceed GitHub's standard file-size limit. Extract these files to their documented locations before running the corresponding analyses.

## HPC and SLURM

The simulation pipelines are designed for execution on an HPC system using SLURM.

The submission scripts (`submit_fba.sh` and `submit_sampling.sh`) create the required SLURM arrays, while `run_fba.sh` and `run_sampling.sh` define the resources and execute the corresponding Python scripts.

Cluster-specific settings, such as Conda environment paths and SLURM resource requests, may need to be adjusted for a different HPC system.

## References
The FBA simulation pipeline is refactored from "Computation of condition-dependent proteome allocation reveals variability in the macro and micro nutrient requirements for growth":


This repository makes use of the following software, models, and methods:

1. **COBRAme**  
   Lloyd, C. J., et al. (2018). COBRAme: A computational framework for genome-scale models of metabolism and gene expression. *PLoS Computational Biology*, 14(7), e1006302.  
   [https://doi.org/10.1371/journal.pcbi.1006302](https://doi.org/10.1371/journal.pcbi.1006302)

2. **iJL1678b ME-model**  
   Lloyd, C. J., et al. (2018). COBRAme: A computational framework for genome-scale models of metabolism and gene expression. *PLoS Computational Biology*, 14(7), e1006302.  
   [https://doi.org/10.1371/journal.pcbi.1006302](https://doi.org/10.1371/journal.pcbi.1006302)

3. **Gurobi Optimizer**  
   Gurobi Optimization, LLC. *Gurobi Optimizer Reference Manual*.  
   [https://www.gurobi.com](https://www.gurobi.com)

4. **solveME**  
   Yang, L., Ma, D., Ebrahim, A., Lloyd, C. J., Saunders, M. A., & Palsson, B. O. (2016).  
   *solveME: fast and reliable solution of nonlinear ME models.*  
   BMC Bioinformatics, 17, 391.  
   [https://doi.org/10.1186/s12859-016-1240-1](https://doi.org/10.1186/s12859-016-1240-1)

5. **Quad MINOS / qMINOS**  
   Ma, D., Yang, L., Fleming, R. M. T., Thiele, I., Palsson, B. O., & Saunders, M. A. (2017).  
   *Reliable and efficient solution of genome-scale models of Metabolism and macromolecular Expression.*  
   Scientific Reports, 7, 40863.  
   [https://doi.org/10.1038/srep40863](https://doi.org/10.1038/srep40863)

6. **FBA simulation pipeline**  
   Lloyd, C. J., Monk, J., Yang, L., Ebrahim, A., & Palsson, B. O. (2021).  
   *Computation of condition-dependent proteome allocation reveals variability in the macro and micro nutrient requirements for growth.*  
   PLOS Computational Biology, 17(6), e1007817.  
   [https://doi.org/10.1371/journal.pcbi.1007817](https://doi.org/10.1371/journal.pcbi.1007817)
