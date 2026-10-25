
from pathlib import Path

import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    OneHotEncoder
)
from sklearn.impute import SimpleImputer

from modules.preprocessing import preprocess_data
from modules.threat_detection import calculate_thresholds


# ==========================================
# DATASET PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_PATH = (
    BASE_DIR / "data" / "raw"
    / "UNSW_NB15_training-set.csv"
)

TEST_PATH = (
    BASE_DIR / "data" / "raw"
    / "UNSW_NB15_testing-set.csv"
)


# ==========================================
# STATISTICAL RULE-BASED EVALUATION
# ==========================================

def evaluate_detection():

    if not TRAIN_PATH.exists():
        raise FileNotFoundError(
            f"Training dataset missing: {TRAIN_PATH}"
        )

    if not TEST_PATH.exists():
        raise FileNotFoundError(
            f"Testing dataset missing: {TEST_PATH}"
        )

    train_df = preprocess_data(
        pd.read_csv(TRAIN_PATH)
    )

    test_df = preprocess_data(
        pd.read_csv(TEST_PATH)
    )

    # Learn thresholds ONLY from training data
    thresholds = calculate_thresholds(train_df)

    test_df["high_bytes"] = (
        test_df["sbytes"] > thresholds["sbytes"]
    )

    test_df["long_duration"] = (
        test_df["dur"] > thresholds["dur"]
    )

    test_df["high_rate"] = (
        test_df["rate"] > thresholds["rate"]
    )

    rule_columns = [
        "high_bytes",
        "long_duration",
        "high_rate"
    ]

    test_df["risk_score"] = (
        test_df[rule_columns].sum(axis=1)
    )

    test_df["predicted_label"] = (
        test_df["risk_score"] >= 1
    ).astype(int)

    y_true = test_df["label"].astype(int)
    y_pred = test_df["predicted_label"]

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(
            y_true, y_pred, zero_division=0
        ),
        "recall": recall_score(
            y_true, y_pred, zero_division=0
        ),
        "f1": f1_score(
            y_true, y_pred, zero_division=0
        )
    }

    matrix = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1]
    )

    report = classification_report(
        y_true,
        y_pred,
        labels=[0, 1],
        target_names=["Normal", "Attack"],
        output_dict=True,
        zero_division=0
    )

    return (
        test_df,
        metrics,
        matrix,
        report,
        thresholds
    )


# ==========================================
# DECISION TREE EVALUATION
# ==========================================

def evaluate_decision_tree():

    if not TRAIN_PATH.exists():
        raise FileNotFoundError(
            f"Training dataset missing: {TRAIN_PATH}"
        )

    if not TEST_PATH.exists():
        raise FileNotFoundError(
            f"Testing dataset missing: {TEST_PATH}"
        )

    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    # Features used by the Decision Tree
    numeric_features = [
        "dur",
        "sbytes",
        "dbytes",
        "rate",
        "spkts",
        "dpkts"
    ]

    categorical_features = [
        "proto",
        "service",
        "state"
    ]

    features = (
        numeric_features + categorical_features
    )

    # Training features and labels
    X_train = train_df[features].copy()
    y_train = train_df["label"].astype(int)

    # Testing features and labels
    X_test = test_df[features].copy()
    y_test = test_df["label"].astype(int)

    # Numeric feature preprocessing
    numeric_transformer = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="median")
        )
    ])

    # Categorical feature preprocessing
    categorical_transformer = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ])

    preprocessor = ColumnTransformer([
        (
            "numeric",
            numeric_transformer,
            numeric_features
        ),
        (
            "categorical",
            categorical_transformer,
            categorical_features
        )
    ])

    # Decision Tree pipeline
    model = Pipeline([
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            DecisionTreeClassifier(
                max_depth=8,
                min_samples_leaf=50,
                class_weight="balanced",
                random_state=42
            )
        )
    ])

    # Train the Decision Tree
    model.fit(X_train, y_train)

    # Predict unseen testing records
    predictions = model.predict(X_test)

    # Calculate performance metrics
    results = {
        "accuracy": accuracy_score(
            y_test, predictions
        ),
        "precision": precision_score(
            y_test,
            predictions,
            zero_division=0
        ),
        "recall": recall_score(
            y_test,
            predictions,
            zero_division=0
        ),
        "f1": f1_score(
            y_test,
            predictions,
            zero_division=0
        )
    }

    matrix = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1]
    )

    return results, matrix
