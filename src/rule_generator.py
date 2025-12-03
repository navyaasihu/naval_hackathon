import pandas as pd
import os
from collections import Counter

ANOMALIES_PATH = os.path.join("data", "anomalies.csv")
RULES_OUTPUT = os.path.join("data", "suggested_rules.txt")

def generate_rules():
    if not os.path.exists(ANOMALIES_PATH):
        print("No anomalies file found. Run detect_anomalies.py first.")
        return

    df = pd.read_csv(ANOMALIES_PATH)

    rules = []

    # Example Rule Type 1: High request rate from same IP to same URL
    grouped = df.groupby(["ip", "url"]).size().reset_index(name="count")
    for _, row in grouped.iterrows():
        if row["count"] >= 3:  # threshold, can tune
            ip = row["ip"]
            url = row["url"]
            rule_text = (
                f"Rule: Possible brute-force or scraping detected.\n"
                f"Condition: IP {ip} made {row['count']} anomalous requests to {url}.\n"
                f"Suggestion: Rate limit or temporarily block IP {ip} for path {url}.\n"
                f"Possible ModSecurity idea: Block if requests_per_minute_from_ip > threshold for {url}.\n"
                "----\n"
            )
            rules.append(rule_text)

    # Example Rule Type 2: Bots with suspicious user agents
    bot_df = df[df.get("is_bot_ua", 0) == 1]
    bot_uas = Counter(bot_df.get("user_agent", []))
    for ua, count in bot_uas.items():
        if count >= 3:
            rule_text = (
                f"Rule: Suspicious bot User-Agent detected.\n"
                f"Condition: User-Agent '{ua}' seen in {count} anomalous requests.\n"
                f"Suggestion: Block or challenge requests with this User-Agent.\n"
                "----\n"
            )
            rules.append(rule_text)

    if not rules:
        print("No strong rule candidates found from anomalies.")
        return

    with open(RULES_OUTPUT, "w") as f:
        for r in rules:
            f.write(r + "\n")

    print(f"Generated {len(rules)} rule suggestions.")
    print(f"Saved to {RULES_OUTPUT}")

if __name__ == "__main__":
    generate_rules()
