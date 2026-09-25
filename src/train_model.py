"""
train_model.py

Trains logistic regression and decision tree classifiers
to predict ICON unit test FAIL from configuration metadata.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

from parse_check_icon import load_synthetic_csv
from build_features import build_feature_matrix


def evaluate(name, model, X, y, cv):
    """Run cross-validated predictions and print metrics."""
    y_pred = cross_val_predict(model, X, y, cv=cv, method="predict")
    y_prob = cross_val_predict(model, X, y, cv=cv, method="predict_proba")[:, 1]

    print(f"\n===== {name} =====")
    print(classification_report(y, y_pred, target_names=["PASS", "FAIL"], digits=3))
    print("Confusion matrix (rows=true, cols=pred):")
    print(confusion_matrix(y, y_pred))
    print(f"ROC-AUC: {roc_auc_score(y, y_prob):.3f}")


def main():
    df = load_synthetic_csv("../data/icon_test_data.csv")
    X, y, preprocessor = build_feature_matrix(df)

    print(f"Training on {X.shape[0]} samples, {X.shape[1]} features")
    print(f"FAIL rate: {y.mean():.1%}")

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    lr = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    evaluate("Logistic Regression", lr, X, y, cv)

    dt = DecisionTreeClassifier(
        max_depth=4, class_weight="balanced", random_state=42
    )
    evaluate("Decision Tree (depth=4)", dt, X, y, cv)

    dt.fit(X, y)
    feature_names = preprocessor.get_feature_names_out()
    print("\n===== Decision Tree Rules =====")
    print(export_text(dt, feature_names=list(feature_names), max_depth=4))


if __name__ == "__main__":
    main()
