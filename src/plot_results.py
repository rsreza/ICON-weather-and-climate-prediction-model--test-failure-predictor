"""
plot_results.py

Generates a figure summarizing model performance:
- Confusion matrices for both models
- ROC curves
- Feature importances from the decision tree
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    confusion_matrix, roc_curve, auc, ConfusionMatrixDisplay
)

from parse_check_icon import load_synthetic_csv
from build_features import build_feature_matrix


def main():
    df = load_synthetic_csv("../data/icon_test_data.csv")
    X, y, preprocessor = build_feature_matrix(df)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    lr = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    dt = DecisionTreeClassifier(max_depth=4, class_weight="balanced", random_state=42)

    lr_prob = cross_val_predict(lr, X, y, cv=cv, method="predict_proba")[:, 1]
    dt_prob = cross_val_predict(dt, X, y, cv=cv, method="predict_proba")[:, 1]

    lr_pred = (lr_prob >= 0.5).astype(int)
    dt_pred = (dt_prob >= 0.5).astype(int)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    # --- Confusion matrices ---
    cm_lr = confusion_matrix(y, lr_pred)
    cm_dt = confusion_matrix(y, dt_pred)
    ConfusionMatrixDisplay(cm_lr, display_labels=["PASS", "FAIL"]).plot(
        ax=axes[0], colorbar=False, cmap="Blues"
    )
    axes[0].set_title("Logistic Regression")

    # --- ROC curves ---
    fpr_lr, tpr_lr, _ = roc_curve(y, lr_prob)
    fpr_dt, tpr_dt, _ = roc_curve(y, dt_prob)
    axes[1].plot(fpr_lr, tpr_lr, label=f"LogReg (AUC={auc(fpr_lr, tpr_lr):.2f})")
    axes[1].plot(fpr_dt, tpr_dt, label=f"Tree (AUC={auc(fpr_dt, tpr_dt):.2f})")
    axes[1].plot([0, 1], [0, 1], "k--", alpha=0.4)
    axes[1].set_xlabel("False Positive Rate")
    axes[1].set_ylabel("True Positive Rate")
    axes[1].set_title("ROC Curves")
    axes[1].legend()

    # --- Feature importances ---
    dt.fit(X, y)
    feature_names = preprocessor.get_feature_names_out()
    importances = dt.feature_importances_
    order = np.argsort(importances)[-10:]  # top 10
    axes[2].barh(
        [feature_names[i] for i in order],
        importances[order],
    )
    axes[2].set_title("Top 10 Decision Tree Features")

    plt.tight_layout()
    plt.savefig("../results_summary.png", dpi=150)
    print("Saved: results_summary.png")


if __name__ == "__main__":
    main()
