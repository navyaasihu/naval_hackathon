import pandas as pd
import numpy as np
from urllib.parse import urlparse
import os

RAW_LOGS_PATH = os.path.join("data", "raw_logs.csv")
FEATURES_PATH = os.path.join("data", "features.csv")

def url_path_length(url: str) -> int:
    try:
        path = urlparse(url).path
        return len(path)
    except Exception:
        return 0

def has_suspicious_chars(url: str) -> int:
    suspicious_chars = ["'", "\"", "<", ">", "(", ")", ";", "--", "/*", "*/"]
    return int(any(c in url for c in suspicious_chars))

def user_agent_is_bot(ua: str) -> int:
    if not isinstance(ua, str):
        return 0
    ua_lower = ua.lower()
    keywords = ["bot", "crawler", "spider", "scanner", "scrapy"]
    return int(any(k in ua_lower for k in keywords))

def extract_features():
    print(f"Loading logs from {RAW_LOGS_PATH}")
    df = pd.read_csv(RAW_LOGS_PATH)

    # --- basic preprocessing ---
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.sort_values("timestamp")

    # Feature 1: path length
    df["url_path_length"] = df["url"].apply(url_path_length)

    # Feature 2: suspicious characters in URL
    df["suspicious_chars"] = df["url"].apply(has_suspicious_chars)

    # Feature 3: is bot user agent
    df["is_bot_ua"] = df["user_agent"].apply(user_agent_is_bot)
    df["minute"] = df["timestamp"].dt.floor("min")
    df["requests_per_min_ip"] = (
        df.groupby(["ip", "minute"])["ip"]
          .transform("count")
    )

    # Feature 5: status code group (2xx, 3xx, 4xx, 5xx)
    df["status_group"] = (df["status"] // 100)

    # Feature 6: response_time_ms and Feature 7: bytes_sent already present

    feature_cols = [
        "url_path_length",
        "suspicious_chars",
        "is_bot_ua",
        "requests_per_min_ip",
        "status_group",
        "response_time_ms",
        "bytes_sent",
    ]

    # Keep original info + features
    out_df = df[["timestamp", "ip", "method", "url", "status"] + feature_cols].copy()

    os.makedirs("data", exist_ok=True)
    out_df.to_csv(FEATURES_PATH, index=False)
    print(f"Saved features to {FEATURES_PATH}")

if __name__ == "__main__":
    extract_features()
