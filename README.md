# ICON Unit Test Failure Predictor

Predicts the probability of PASS/FAIL for ICON unit tests based on
configuration metadata (MPI, compiler, process count, build type).

## Motivation

DKRZ signaled a need for "AI-supported tools for ICON developers" --
specifically for interpreting test results and providing CI feedback.
This tool addresses that need by learning patterns from historical
test outcomes.

## Status

- Parser: works with real `make check-icon` output.
- Data source: synthetic data was used for development because the
  local Docker build of ICON failed at the final compilation step
  due to a gfortran/MPI module version mismatch (container's mpi.mod
  built with gfortran 15, ICON uses gfortran 13). The parser is
  designed to work with real ICON output without changes.

## Install

    pip install -r requirements.txt

## Usage

    python3 generate_data.py
    cd src && python3 train_model.py
    python3 predict.py

## Files

| File | Purpose |
|---|---|
| src/parse_check_icon.py | Parse real `make check-icon` output |
| src/build_features.py | Encode configuration metadata |
| src/train_model.py | Train and evaluate classifier |
| src/predict.py | Predict for a new configuration |
| data/icon_test_data.csv | Synthetic training data |

## Method

- Features: test name, variant, compiler, MPI enabled, process count,
  build type (one-hot encoded for categoricals).
- Models: logistic regression (baseline) and decision tree (depth 4).
- Validation: 5-fold stratified cross-validation.
- Metrics: precision, recall, F1, ROC-AUC, confusion matrix.

## Limitations

- Synthetic data does not capture real ICON test behavior.
- Small dataset (360 records, 25 failures).
- SKIP outcomes are excluded from classification.
