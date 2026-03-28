from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier, StackingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


FEATURES = [
    "device_type",
    "traffic_source",
    "location",
    "cart_value",
    "discount_pct",
    "page_load_seconds",
]
TARGET = "is_purchase"



def build_preprocessor() -> ColumnTransformer:
    categorical_cols = ["device_type", "traffic_source", "location"]
    numeric_cols = ["cart_value", "discount_pct", "page_load_seconds"]

    categorical_pipe = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="most_frequent")), ("ohe", OneHotEncoder(handle_unknown="ignore"))]
    )
    numeric_pipe = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )

    return ColumnTransformer(
        transformers=[("categorical", categorical_pipe, categorical_cols), ("numeric", numeric_pipe, numeric_cols)]
    )



def evaluate(y_true: np.ndarray, probs: np.ndarray) -> dict[str, float]:
    preds = (probs >= 0.5).astype(int)
    return {
        "roc_auc": float(roc_auc_score(y_true, probs)),
        "pr_auc": float(average_precision_score(y_true, probs)),
        "f1": float(f1_score(y_true, preds)),
    }



def train(data_path: Path, model_dir: Path, test_size: float, random_state: int) -> None:
    df = pd.read_csv(data_path)
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    preprocessor = build_preprocessor()

    baseline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )

    advanced = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            (
                "classifier",
                StackingClassifier(
                    estimators=[
                        ("rf", RandomForestClassifier(n_estimators=250, max_depth=8, random_state=random_state)),
                        ("hgb", HistGradientBoostingClassifier(max_depth=5, learning_rate=0.06, random_state=random_state)),
                    ],
                    final_estimator=LogisticRegression(max_iter=800),
                    stack_method="predict_proba",
                    passthrough=False,
                ),
            ),
        ]
    )

    baseline.fit(X_train, y_train)
    advanced.fit(X_train, y_train)

    baseline_probs = baseline.predict_proba(X_test)[:, 1]
    advanced_probs = advanced.predict_proba(X_test)[:, 1]

    baseline_metrics = evaluate(y_test.to_numpy(), baseline_probs)
    advanced_metrics = evaluate(y_test.to_numpy(), advanced_probs)

    if advanced_metrics["roc_auc"] >= baseline_metrics["roc_auc"]:
        best_name = "stacked_ensemble"
        best_model = advanced
        best_metrics = advanced_metrics
    else:
        best_name = "logistic_regression"
        best_model = baseline
        best_metrics = baseline_metrics

    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, model_dir / "best_model.joblib")

    report = {
        "features": FEATURES,
        "target": TARGET,
        "best_model": best_name,
        "baseline_metrics": baseline_metrics,
        "advanced_metrics": advanced_metrics,
        "best_metrics": best_metrics,
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
    }

    with open(model_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))



def main() -> None:
    parser = argparse.ArgumentParser(description="Train baseline and advanced ML models for funnel conversion.")
    parser.add_argument("--data-path", type=Path, default=Path("data/train.csv"))
    parser.add_argument("--model-dir", type=Path, default=Path("models"))
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    train(args.data_path, args.model_dir, args.test_size, args.random_state)


if __name__ == "__main__":
    main()
