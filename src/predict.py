"""
predict.py

Given a configuration, output the predicted probability of FAIL.
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression

from parse_check_icon import load_synthetic_csv
from build_features import build_feature_matrix


def train_final_model():
    df = load_synthetic_csv("../data/icon_test_data.csv")
    X, y, preprocessor = build_feature_matrix(df)
    model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    model.fit(X, y)
    return model, preprocessor


def predict_one(model, preprocessor, config: dict) -> float:
    """Return probability of FAIL for a single configuration."""
    row = pd.DataFrame([config])
    X = preprocessor.transform(row)
    return float(model.predict_proba(X)[0, 1])


if __name__ == "__main__":
    model, preprocessor = train_final_model()

    examples = [
        {
            "test_name": "test_index_list",
            "variant": "mpi",
            "compiler": "gcc-13.3.0",
            "mpi_enabled": True,
            "nproc": 8,
            "build_type": "debug",
        },
        {
            "test_name": "test_kind",
            "variant": "plain",
            "compiler": "intel-2021.5.0",
            "mpi_enabled": False,
            "nproc": 1,
            "build_type": "release",
        },
    ]

    print("Configuration -> P(FAIL)")
    print("-" * 60)
    for cfg in examples:
        prob = predict_one(model, preprocessor, cfg)
        print(f"{cfg['test_name']:25s} nproc={cfg['nproc']} "
              f"compiler={cfg['compiler']:15s} -> {prob:.1%}")
