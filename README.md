# PhosKinTime
 
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15351017.svg)](https://doi.org/10.5281/zenodo.15351017)

**PhosKinTime** is an ODE-based modeling package for analyzing phosphorylation dynamics over time. It integrates
parameter estimation, sensitivity analysis, steady-state computation, and visualization tools to help researchers
explore kinase-substrate interactions in a temporal context.

## Acknowledgments

This project originated as part of my master's thesis work at Theoretical Biophysics group (
now, [Klipp-Linding Lab](https://www.klipp-linding.science/tbp/index.php/en/)), Humboldt Universität zu Berlin.

- **Conceptual framework and mathematical modeling** were developed under the supervision of **[Prof. Dr. Dr. H.C. Edda Klipp](https://www.klipp-linding.science/tbp/index.php/en/people/51-people/head/52-klipp)**.
- **Experimental datasets** were provided by the **[(Retd. Prof.) Dr. Rune Linding](https://www.klipp-linding.science/tbp/index.php/en/people/51-people/head/278-rune-linding)**.
- The subpackage `tfopt` is an optimized and efficient derivative
  of [original work](https://github.com/Normann-BPh/Transcription-Optimization) by my colleague **[Julius Normann](https://github.com/Normann-BPh)**, adapted with permission.

I am especially grateful
to [Ivo Maintz](https://rumo.biologie.hu-berlin.de/tbp/index.php/en/people/54-people/6-staff/60-maintz) for his generous
technical support, enabling seamless experimentation with packages and server setups.

## Overview

PhosKinTime uses ordinary differential equations (ODEs) to model phosphorylation kinetics and supports multiple
mechanistic hypotheses, including:

- **Distributive Model:** Phosphorylation events occur independently.
- **Successive Model:** Phosphorylation events occur sequentially.
- **Random Model:** Phosphorylation events occur in a random manner.

The package is designed with modularity in mind. It consists of several key components:

- **Configuration:** Centralized settings (paths, parameter bounds, logging, etc.) are defined in the config module.
- **Models:** Different ODE models (distributive, successive, random) are implemented to simulate phosphorylation.
- **Parameter Estimation:** Multiple routines (sequential and normal estimation) estimate kinetic parameters from
  experimental data.
- **Sensitivity Analysis:** Morris sensitivity analysis is used to evaluate the influence of each parameter on the model
  output.
- **Steady-State Calculation:** Functions compute steady-state initial conditions for ODE simulation.
- **Utilities:** Helper functions support file handling, data formatting, report generation, and more.
- **Visualization:** A comprehensive plotting module generates static and interactive plots to visualize model fits,
  parameter profiles, PCA, t-SNE, and sensitivity indices.

## Installation

This guide provides clean setup instructions for running the `phoskintime` package on a new machine. Choose the scenario
that best fits your environment and preferences. 
 
Before proceeding, ensure you have the following prerequisites installed: 
 
- graphviz (for generating diagrams)   

```bash 
# For Debian/Ubuntu
sudo apt-get install graphviz   

# For Fedora
sudo dnf install graphviz    

# For MacOS
brew install graphviz 
``` 

- python 3.10 or higher 

```bash  
# Check python version 
python3 --version  

# If not installed, install python 3.10 or higher 

# For Debian/Ubuntu  
sudo apt-get install python3.10 
 
# For Fedora 
sudo dnf install python3.10 

# For MacOS
brew install python@3.10
``` 

- git (for cloning the repository) 
 
```bash  
# For Debian/Ubuntu 
sudo apt-get install git  

# For Fedora 
sudo dnf install git  

# For MacOS 
brew install git 
```

---

## Scenario 1: pip + virtualenv (Debian/Ubuntu/Fedora)

### For **Debian/Ubuntu**

```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git
```

### For **Fedora**

```bash
sudo dnf install -y python3 python3-pip python3-virtualenv git
```

### Setup

```bash
git clone git@github.com:bibymaths/phoskintime.git
cd phoskintime

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Scenario 2: Poetry + `pyproject.toml`

### Install Poetry (all platforms)

```bash
curl -sSL https://install.python-poetry.org | python3 -
# Or: pip install poetry
```

### Setup

```bash
git clone git@github.com:bibymaths/phoskintime.git
cd phoskintime

# Install dependencies
poetry install

# Optional: activate shell within poetry env
poetry shell
```

---

## Scenario 3: Using [`uv`](https://github.com/astral-sh/uv) (fast, isolated pip alternative)

### Install `uv`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup

```bash
git clone git@github.com:bibymaths/phoskintime.git
cd phoskintime

# Create virtual environment and install deps fast
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

---

## Scenario 4: Conda or Mamba (Anaconda/Miniconda users)

### Setup

```bash
git clone git@github.com:bibymaths/phoskintime.git
cd phoskintime

# Create and activate conda environment
conda create -n phoskintime python=3.10 -y
conda activate phoskintime

# Install dependencies
pip install -r requirements.txt
```

Or if using `pyproject.toml`, add:

```bash
pip install poetry
poetry install
```

For making illustration diagrams, you need to install Graphviz. You can do this via conda or apt-get:

```bash 
conda install graphviz
``` 

or

```bash 
apt-get install graphviz
``` 

or download it from the [Graphviz website](https://graphviz.gitlab.io/download/).
For macusers, you can use Homebrew:

```bash  
brew install graphviz
``` 

The package is executed via the main script located in the `bin` directory. This script sets up the configuration,
processes experimental data, performs parameter estimation, generates model simulations, and creates a comprehensive
report.

### Main Script

The command-line arguments (such as parameter bounds, fixed parameters, bootstrapping iterations, and input file paths)
are parsed by the configuration module. The main script then:

- Loads the experimental data.
- Logs the configuration and initializes output directories.
- Processes each gene in parallel using a ProcessPoolExecutor.
- Performs parameter estimation (toggling between sequential and normal modes as configured).
- Generates ODE simulations and various plots.
- Saves all results (including a global HTML report) in the designated output directory.

# Command-Line Entry Point for the Phoskintime Pipeline

The `phoskintime` pipeline provides a command-line interface to execute various stages of the workflow,  
including preprocessing, optimization, and modeling. Below are the usage instructions and examples for running  
the pipeline.

Before running any commands, ensure you are in the working directory one level above the project root (where the project  
directory is visible).

### Run All Stages
Run the entire pipeline with the default (local) solver:
```bash
python phoskintime all
```

### Run Preprocessing Only
Execute only the preprocessing stage:
```bash
python phoskintime prep
```

### Run Transcription-Factor-mRNA Optimization (TFOPT)
Run TFOPT with the local solver:
```bash
python phoskintime tfopt --mode local
```

Run TFOPT with the evolutionary solver:
```bash
python phoskintime tfopt --mode evol
```

### Run Kinase-Phosphorylation Optimization (KINOPT)
Run KINOPT with the local solver:
```bash
python phoskintime kinopt --mode local
```

Run KINOPT with the evolutionary solver:
```bash
python phoskintime kinopt --mode evol
```

### Run the Model
Execute the modeling stage:
```bash
python phoskintime model
```

### Example

Here’s a brief overview of the execution flow:

1. **Configuration:**
    - `config/config.py` and `config/constants.py` set up model options (e.g., `ODE_MODEL`, `ESTIMATION_MODE`), time
      points, file paths, and logging settings.
    - Command-line arguments are parsed to override default settings.

2. **Parameter Estimation:**
    - Depending on the chosen estimation mode (sequential or normal), functions from `paramest/seqest.py` or
      `paramest/normest.py` are used.
    - The toggle functionality in `paramest/toggle.py` selects the appropriate routine.
    - Results are saved and passed for visualization.

3. **Model Simulation and Visualization:**
    - The selected ODE model (from `models/`) is used to simulate system dynamics.
    - The `plotting` module generates plots (e.g., parallel coordinates, PCA, t-SNE, model fits, and sensitivity plots)
      to visually inspect the results.

4. **Reporting:**
    - The `utils/display.py` and `utils/tables.py` modules save results and generate an HTML report summarizing the
      analysis.

## Modules

- **Config Module:**
    - `config/constants.py`: Global constants (model settings, time points, directories, scoring weights, etc.).
    - `config/config.py`: Command-line argument parsing and configuration extraction.
    - `config/logconf.py`: Logging configuration with colored console output and rotating file logs.
    - `config/helpers/__init__.py`: Helper functions for generating parameter names, state labels, bounds, and clickable
      file links.

- **Models Module:**  
  Implements various ODE models:
    - `randmod.py`: Random model with vectorized state calculations.
    - `distmod.py`: Distributive model.
    - `succmod.py`: Successive model.
    - `weights.py`: Weighting schemes for parameter estimation.

- **Parameter Estimation Module:**
    - `normest.py`: Normal (all timepoints at once) estimation.
    - `toggle.py`: Utility to switch between estimation modes.
    - `core.py`: Integrates estimation, ODE solving, error metrics, and visualization.

- **Steady-State Module:**
    - `initdist.py`, `initrand.py`, `initsucc.py`: Compute steady-state initial conditions for each model type.

- **Sensitivity Module:**
    - `analysis.py`: Implements Morris sensitivity analysis, including problem definition, sampling, analysis, and
      plotting of sensitivity indices.

- **Utils Module:**
    - `display.py`: Helper functions for file/directory management, data loading, result saving, and report generation.
    - `tables.py`: Functions to generate, save, and compile data tables (LaTeX and CSV).

- **Bin Module:**
    - `main.py`: The main entry point that orchestrates the entire workflow—from configuration and data loading to
      parameter estimation, simulation, visualization, and report generation.

## Customization

You can customize the package by:

- Adjusting model parameters and bounds in the config files.
- Choosing the ODE model type by modifying `ODE_MODEL` in `constants.py`.
- Configuring output directories and file paths.
- Modifying the logging behavior in `logconf.py`.
- Tweaking the scoring function weights in `constants.py`.

---

PhosKinTime is a flexible and powerful package for modeling phosphorylation kinetics. Its modular design allows
researchers to simulate different mechanistic models, estimate kinetic parameters, analyze parameter sensitivity, and
generate comprehensive visual and tabular reports. Whether you are exploring basic kinetic hypotheses or conducting
in-depth sensitivity analysis, PhosKinTime offers the necessary tools for robust model-based analysis.

For more information, please refer to the individual module documentation and source code.

## License

This package is distributed under the BSD 3-Clause License.  
See the [LICENSE](./LICENSE) file for full details.

--- 

[//]: # (![Goal]&#40;static/images/goal_2.png&#41;)
