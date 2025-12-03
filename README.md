# NavGuard ML

Adaptive Machine Learning-Based Web Traffic Anomaly Detection System

NavGuard ML is a cyber security project that uses Machine Learning to detect abnormal web traffic behavior and automatically suggest firewall rules. The system helps existing Web Application Firewalls (WAF) identify unknown attacks and reduce manual rule writing by security teams.

---

## Problem Statement

Traditional web firewalls depend on static and predefined rules. These rules are effective only for known attacks. When new or modified threats appear, security teams must manually analyze logs and update rules.

Organizations face the following challenges:

* Failure to detect unknown attacks
* Too many false alerts
* Manual and slow rule updates
* High workload on security teams

---

## Solution Overview

NavGuard ML analyzes traffic patterns using Machine Learning instead of depending only on fixed security rules. The system learns what normal activity looks like and automatically marks suspicious behavior as abnormal.

### Features

* Detects abnormal traffic using Machine Learning
* Works alongside existing WAF systems
* Explains why a request was considered dangerous
* Suggests firewall rules automatically
* Provides a web-based dashboard for monitoring
* Designed for continuous improvement through feedback


---

## Tech Stack

| Category         | Technology                      |
|------------------|----------------------------------|
| Language         | Python                           |
| Machine Learning | Isolation Forest (Scikit-learn)  |
| Dashboard        | Streamlit                        |
| Data Processing  | Pandas                           |
| Storage          | CSV Files                        |
| Deployment       | Docker                           |
| Firewall Support | ModSecurity (conceptual)         |
| OS               | Linux / Windows                  |

---

## Folder Structure

navguard_ml/

|

├── data/

│ ├── raw_logs.csv

│ ├── features.csv

│ ├── anomalies.csv

│ └── suggested_rules.txt

|

├── models/

│ ├── isolation_forest.pkl

│ └── scaler.pkl

|

├── src/

│ ├── log_generator.py

│ ├── feature_extractor.py

│ ├── train_model.py

│ ├── detect_anomalies.py

│ ├── rule_generator.py

│ └── dashboard_app.py

|

├── requirements.txt

└── README.md


---

## Installation

## Install dependencies
pip install -r requirements.txt

## Step 1: Generate Web Traffic Logs (creates simulated traffic containing both normal activity and attack behavior)
python src/log_generator.py

## Step 2: Extract Features (converts raw logs into numerical values required for ML processing)
python src/feature_extractor.py

## Step 3: Train the Machine Learning Model (trains the Isolation Forest model using web traffic data)
python src/train_model.py

## Detect anomalies and save it in data/anomalies.csv
python src/detect_anomalies.py

## Generate Firewall Rule Suggestions and are saved in data/suggested_rules.txt
python src/rule_generator.py

## Launch Dashboard 
streamlit run src/dashboard_app.py



