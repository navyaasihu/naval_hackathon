import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

FEATURES_PATH = os.path.join("data", "features.csv")
MODEL_PATH = os.path.join("models", "isolation_forest.pkl")
SCALER_PATH = os.path.join("models", "scaler.pkl")

def train_model():
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

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,  # assume ~5% anomalies
        random_state=42,
        n_jobs=-1
    )

    print("Training Isolation Forest model...")
    model.fit(X_scaled)
    print("Training complete.")

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved scaler to {SCALER_PATH}")

if __name__ == "__main__":
    train_model()
