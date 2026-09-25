"""
build_features.py

Converts the parsed ICON test data into a numeric feature matrix
suitable for scikit-learn models.
"""

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


CATEGORICAL_FEATURES = ["test_name", "variant", "compiler", "build_type"]
NUMERIC_FEATURES = ["mpi_enabled", "nproc"]


def build_feature_matrix(df: pd.DataFrame):
    """Returns (X, y, preprocessor)."""
    df = df[df["result"].isin(["PASS", "FAIL"])].copy()

    y = (df["result"] == "FAIL").astype(int).values

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("num", "passthrough", NUMERIC_FEATURES),
        ]
    )

    X = preprocessor.fit_transform(df[CATEGORICAL_FEATURES + NUMERIC_FEATURES])
    return X, y, preprocessor


if __name__ == "__main__":
    from parse_check_icon import load_synthetic_csv
    import numpy as np

    df = load_synthetic_csv("../data/icon_test_data.csv")
    X, y, prep = build_feature_matrix(df)
    print(f"Feature matrix shape: {X.shape}")
    print(f"Label distribution: {dict(zip(*np.unique(y, return_counts=True)))}")
