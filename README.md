```markdown
# ICON Unit Test Failure Predictor

A machine learning approach to predicting unit test outcomes for the ICON weather and climate model.

## Table of Contents

- [Introduction to ICON](#introduction-to-icon)
- [The Problem](#the-problem)
- [Proposed Solution](#proposed-solution)
- [Method](#method)
- [Data](#data)
- [Results](#results)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Limitations](#limitations)
- [Author](#author)
- [License](#license)

---

## Introduction to ICON

ICON (ICOsahedral Nonhydrostatic) is a flexible, scalable, high-performance modelling framework for weather, climate, and environmental prediction. It is developed through a partnership between the Max Planck Institute for Meteorology (MPI-M), the German Weather Service (DWD), the German Climate Computing Center (DKRZ), ETH Zurich, and the Karlsruhe Institute of Technology (KIT).

The model uses an icosahedral grid structure, which avoids the pole problems common in traditional latitude-longitude grids and allows for efficient scaling on modern supercomputers, including GPU-based systems. ICON is used operationally for weather forecasting in Germany and Switzerland and serves as a central research tool for climate modelling.

**Reference:**

> ICON Website. *About ICON*. https://www.icon-model.org

---

## The Problem

ICON includes a unit testing framework that validates individual subroutines and modules in the codebase. When developers run `make check-icon`, each test reports one of three outcomes: **PASS**, **SKIP**, or **FAIL**.

With hundreds of tests running across multiple configurations — different compilers, MPI settings, process counts, and build types — a failing CI run can produce a large amount of output. Developers must scan through all results to identify which tests failed and why.

The core question of this project is:

> **Can we predict which tests are likely to fail, based only on their configuration metadata, before they are even run?**

If the answer is yes, developers can prioritize their debugging, and CI systems can highlight high-risk tests automatically.

---

## Proposed Solution

This project provides a complete machine learning pipeline that:

1. **Parses ICON unit test output** — extracts `PASS`, `SKIP`, and `FAIL` results from `make check-icon` logs into a structured format.
2. **Learns patterns** — trains classifiers to associate configuration metadata (test name, compiler, MPI settings, process count, build type) with failure probability.
3. **Predicts outcomes** — for any given configuration, outputs the probability of a test failing.

The tool is designed to work with **real ICON test logs**. A parser (`src/parse_check_icon.py`) handles the exact output format produced by `make check-icon`.

---

## Method

### Models

Two interpretable classifiers were used:

- **Logistic Regression** — a simple linear baseline that provides calibrated probability estimates.
- **Decision Tree (max depth 4)** — produces human-readable rules that explain which configurations are associated with failures.

### Features

| Feature | Type | Example Values |
|---|---|---|
| `test_name` | Categorical | `test_index_list`, `test_kind` |
| `variant` | Categorical | `plain`, `mpi`, `nompi` |
| `compiler` | Categorical | `gcc-13.3.0`, `gcc-11.2.0`, `intel-2021.5.0` |
| `mpi_enabled` | Binary | `True`, `False` |
| `nproc` | Numeric | `1`, `4`, `8` |
| `build_type` | Categorical | `debug`, `release` |

### Validation

- **5-fold stratified cross-validation** to ensure reliable estimates on a small dataset.
- **Metrics:** Precision, Recall, F1-score, ROC-AUC, and Confusion Matrix.

### Tools

Python 3.10, scikit-learn, pandas, matplotlib, NumPy.

---

## Data

### Source

The pipeline is designed to parse **real `make check-icon` output**. The parser matches lines of the form:

```
PASS: test_divide_cell
SKIP: test_divide_cell.mpi
FAIL: test_index_list
```

### Synthetic Data

This repository uses **synthetic data** to demonstrate the pipeline. The synthetic dataset mimics the structure and format of real ICON test outputs, including configuration-dependent failure patterns.

The synthetic data was generated to allow development and testing of the machine learning pipeline without requiring access to a full ICON installation or production CI logs.

**Important:** The parser works with real ICON output without modification. To train the model on real data in the future, simply replace `data/icon_test_data.csv` with a CSV produced by `src/parse_check_icon.py` on real `make check-icon` logs. No code changes are required.

---

## Results

![Model performance summary](results_summary.png)

---

## Project Structure

```
.
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── generate_data.py           # Synthetic data generator
├── results_summary.png        # Model performance figure
├── LICENSE                    # MIT License
├── .gitignore
├── data/
│   └── icon_test_data.csv     # Training data (synthetic)
└── src/
    ├── parse_check_icon.py    # Parse real make check-icon output
    ├── build_features.py      # Feature encoding
    ├── train_model.py         # Train and evaluate models
    ├── predict.py             # Predict for new configurations
    └── plot_results.py        # Generate results figure
```

---

## Installation

```bash
git clone https://github.com/rsreza/ICON-weather-and-climate-prediction-model--test-failure-predictor.git
cd ICON-weather-and-climate-prediction-model--test-failure-predictor

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt`:

```
pandas>=2.0
scikit-learn>=1.3
matplotlib>=3.7
numpy>=1.24
```

---

## Usage

All commands assume the virtual environment is activated.

### 1. Generate the synthetic dataset

```bash
python3 generate_data.py
```

### 2. Train and evaluate the models

```bash
cd src
python3 train_model.py
```

### 3. Generate the results figure

```bash
python3 plot_results.py
```

### 4. Predict for a new configuration

```bash
python3 predict.py
```

Example output:

```
Configuration -> P(FAIL)
------------------------------------------------------------
test_index_list           nproc=8 compiler=gcc-13.3.0      -> 96.4%
test_kind                 nproc=1 compiler=intel-2021.5.0  ->  1.8%
```

### 5. Parse real ICON output

```python
from src.parse_check_icon import parse_check_icon_output

with open("real_check_icon_output.txt") as f:
    df = parse_check_icon_output(f.read())

print(df)
```

Save the resulting DataFrame to `data/icon_test_data.csv` and rerun the pipeline.

---

## Limitations

- **Synthetic data:** The training data is generated, not from real ICON runs. Patterns and metrics reflect the generator's design.
- **Small dataset:** 306 records, 34 failures.
- **SKIP outcomes excluded:** Predicting SKIP is a separate problem.
- **Real logs will be noisier:** Class imbalance and noise are likely larger in production, and recall may drop.

The contribution is demonstrating the **full pipeline** for AI-assisted test diagnostics — parser, feature encoding, model, evaluation, and reporting — with a clear path to real ICON data.

---

## Author

**Reza Kahndan**
GitHub: [@rsreza](https://github.com/rsreza)
Email: rs.reza_kahndan@ut.ac.ir

---

## License

MIT License. See `LICENSE` for details.
```
