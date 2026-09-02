# Project description

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
4. `scripts/FBA/` — scripts for substrate-specific FBA simulations using Gurobi or QMINOS.
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

qMINOS is not distributed with this repository and requires access to the qMINOS source code, which can be obtained from Prof. Michael A. Saunders at Stanford University. Detailed instructions for obtaining, installing, and configuring qMINOS and solvemepy are provided in [`docs/qminos-solver-installation.md`](docs/qminos-solver-installation.md).

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

### 2. Submit sampling jobs

Without an alternative carbon source:

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

## Data

Some datasets required by the analysis may be distributed as compressed archives because individual files exceed GitHub's standard file-size limit. Extract these files to their documented locations before running the corresponding analyses.

## HPC and SLURM

The simulation pipelines are designed for execution on an HPC system using SLURM.

The submission scripts (`submit_fba.sh` and `submit_sampling.sh`) create the required SLURM arrays, while `run_fba.sh` and `run_sampling.sh` define the resources and execute the corresponding Python scripts.

Cluster-specific settings, such as Conda environment paths and SLURM resource requests, may need to be adjusted for a different HPC system.

## References
