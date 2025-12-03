import streamlit as st
import pandas as pd
import os

FEATURES_PATH = os.path.join("data", "features.csv")
ANOMALIES_PATH = os.path.join("data", "anomalies.csv")
RULES_OUTPUT = os.path.join("data", "suggested_rules.txt")

def load_csv_safe(path):
    if not os.path.exists(path):
        return None
    return pd.read_csv(path)

def main():
    st.title("NavGuard ML – Web Traffic Anomaly Dashboard")

    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Go to", ["Overview", "Anomalies", "Rule Suggestions"])

    if page == "Overview":
        st.subheader("Traffic Overview")
        df = load_csv_safe(FEATURES_PATH)
        if df is None:
            st.warning("No features file found. Run feature_extractor.py first.")
            return
        st.write(f"Total requests: {len(df)}")
        st.dataframe(df.head(20))

    elif page == "Anomalies":
        st.subheader("Detected Anomalies")
        anomalies = load_csv_safe(ANOMALIES_PATH)
        if anomalies is None or anomalies.empty:
            st.info("No anomalies file found or no anomalies detected.")
            return
        st.write(f"Total anomalies: {len(anomalies)}")
        st.dataframe(anomalies[["timestamp", "ip", "method", "url", "status", "anomaly_score"]].head(50))

    elif page == "Rule Suggestions":
        st.subheader("Suggested Rules")
        if not os.path.exists(RULES_OUTPUT):
            st.info("No suggested_rules.txt file found. Run rule_generator.py first.")
            return
        with open(RULES_OUTPUT, "r") as f:
            content = f.read()
        st.text_area("Rule Suggestions", value=content, height=300)

if __name__ == "__main__":
    main()
