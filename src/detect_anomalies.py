import pandas as pd
import numpy as np
import joblib
import os

FEATURES_PATH = os.path.join("data", "features.csv")
MODEL_PATH = os.path.join("models", "isolation_forest.pkl")
SCALER_PATH = os.path.join("models", "scaler.pkl")

ANOMALIES_OUTPUT = os.path.join("data", "anomalies.csv")

def detect_anomalies():
    print(f"Loading features from {FEATURES_PATH}")
    df = pd.read_csv(FEATURES_PATH)

    feature_cols = [
        "url_path_length",
        "suspicious_chars",
        "is_bot_ua",
        "requests_per_min_ip",
        "status_group",
        "response_time_ms",
        "bytes_sent",
    ]

    X = df[feature_cols].values

    print("Loading model and scaler...")
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    X_scaled = scaler.transform(X)

    # IsolationForest: predict returns 1 for normal, -1 for anomaly
    print("Scoring anomalies...")
    preds = model.predict(X_scaled)
    scores = model.decision_function(X_scaled)  # smaller = more anomalous

    df["anomaly_label"] = preds
    df["anomaly_score"] = scores

    # Anomalies: label == -1
    anomalies = df[df["anomaly_label"] == -1].copy()
    anomalies = anomalies.sort_values("anomaly_score")

    print(f"Found {len(anomalies)} anomalies.")
    anomalies.to_csv(ANOMALIES_OUTPUT, index=False)
    print(f"Saved anomalies to {ANOMALIES_OUTPUT}")

if __name__ == "__main__":
    detect_anomalies()
