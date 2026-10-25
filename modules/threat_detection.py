
import pandas as pd


FEATURES = ["sbytes", "dur", "rate"]


def calculate_thresholds(df):
    """
    Calculate reference thresholds using records
    labeled as normal network traffic.
    """
    normal_data = df[df["label"] == 0]

    if normal_data.empty:
        raise ValueError("No normal records found.")

    thresholds = {}

    for feature in FEATURES:
        values = pd.to_numeric(
            normal_data[feature],
            errors="coerce"
        ).dropna()

        if values.empty:
            raise ValueError(
                f"No valid values for {feature}"
            )

        thresholds[feature] = values.quantile(0.99)

    return thresholds


def detect_threats(df):
    """
    Identify unusual network behavior using
    statistical threshold-based rules.
    """
    df = df.copy()

    thresholds = calculate_thresholds(df)

    # Individual rule flags
    df["high_bytes"] = (
        df["sbytes"] > thresholds["sbytes"]
    )

    df["long_duration"] = (
        df["dur"] > thresholds["dur"]
    )

    df["high_rate"] = (
        df["rate"] > thresholds["rate"]
    )

    rule_columns = [
        "high_bytes",
        "long_duration",
        "high_rate"
    ]

    # Calculate number of triggered rules
    df["risk_score"] = (
        df[rule_columns].sum(axis=1)
    )

    # Assign risk level
    def assign_risk(score):
        if score >= 2:
            return "High"
        elif score == 1:
            return "Medium"
        return "Low"

    df["risk_level"] = (
        df["risk_score"].apply(assign_risk)
    )

    # Identify suspicious events
    df["suspicious"] = df["risk_score"] >= 1

    # Generate understandable explanations
    def explain_risk(row):
        reasons = []

        if row["high_bytes"]:
            reasons.append("Unusual traffic volume")

        if row["long_duration"]:
            reasons.append("Long connection duration")

        if row["high_rate"]:
            reasons.append("Unusually high traffic rate")

        if not reasons:
            return "No anomaly detected"

        return ", ".join(reasons)

    df["alert_reason"] = df.apply(
        explain_risk,
        axis=1
    )

    return df, thresholds
