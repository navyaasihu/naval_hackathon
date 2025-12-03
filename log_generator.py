import csv
import random
from datetime import datetime, timedelta

OUTPUT_FILE = "data/raw_logs.csv"

NORMAL_IPS = ["10.0.0." + str(i) for i in range(2, 50)]
ATTACKER_IPS = ["192.168.1.100", "192.168.1.101"]

URLS_NORMAL = ["/", "/home", "/products", "/about", "/contact", "/profile", "/cart"]
URLS_SENSITIVE = ["/admin", "/login", "/reset-password", "/api/data"]
URLS_ATTACK = ["/admin", "/login", "/api/data", "/backup"]

USER_AGENTS = [
    "Mozilla/5.0",
    "Chrome/118.0",
    "Safari/537.36",
    "Edge/120",
    "Firefox/122"
]

BOT_AGENTS = [
    "BadBot/1.0",
    "Scrapy/2.0",
    "CrawlerX",
    "ScannerPro"
]

METHODS = ["GET", "POST"]

def random_timestamp(start):
    return start + timedelta(seconds=random.randint(0, 3600))

def generate_logs(total=3000):
    start_time = datetime.now() - timedelta(hours=1)

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "ip", "method", "url", "status", "response_time_ms", "bytes_sent", "user_agent"])

        for _ in range(total):

            is_attack = random.random() < 0.15   # 15% attack traffic

            if is_attack:
                ip = random.choice(ATTACKER_IPS)
                url = random.choice(URLS_ATTACK)
                ua = random.choice(BOT_AGENTS)
                status = random.choice([401, 403, 500])
                response_time = random.randint(10, 60)
                bytes_sent = random.randint(100, 600)
            else:
                ip = random.choice(NORMAL_IPS)
                url = random.choice(URLS_NORMAL + URLS_SENSITIVE)
                ua = random.choice(USER_AGENTS)
                status = random.choice([200, 200, 200, 301, 404])
                response_time = random.randint(80, 300)
                bytes_sent = random.randint(1500, 6000)

            timestamp = random_timestamp(start_time)
            method = random.choice(METHODS)

            writer.writerow([
                timestamp.isoformat(),
                ip,
                method,
                url,
                status,
                response_time,
                bytes_sent,
                ua
            ])

    print(f"Generated {total} traffic logs in {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_logs(total=5000)  # You can change this number
