
# 🛡️ CyberWatch
## Stream-Based Cybersecurity Threat Analytics and Visualization Platform

CyberWatch is a Big Data Analytics Course-Based Project that
analyzes cybersecurity network traffic, identifies suspicious
activities, simulates event streams, and visualizes security
insights through an interactive dashboard.

The application uses the UNSW-NB15 dataset, statistical
threshold-based detection, and a Decision Tree classifier
to analyze and evaluate network security events.

## 🎯 Problem Statement

Organizations generate large volumes of network traffic and
security logs. Manually analyzing these records to identify
suspicious behavior can be difficult and time-consuming.

CyberWatch provides a data-driven platform for exploring
network traffic, detecting potential threats, and generating
interpretable security analytics.

## 🚀 Key Features

### 1. Security Overview
- Total network event statistics
- Normal versus attack traffic distribution
- Attack category analysis
- Interactive network traffic visualizations

### 2. Threat Detection
- Statistical threshold-based detection
- Risk scoring and severity categorization
- Explainable security alerts
- Suspicious event filtering

### 3. Live Threat Simulation
- Historical network event replay
- Start, Pause, and Reset controls
- Adjustable event processing speed
- Dynamically updated monitoring charts
- Simulated security alerts

### 4. Detection Evaluation
- Statistical rule-based evaluation
- Decision Tree classifier
- Accuracy, precision, recall, and F1-score
- Confusion matrix visualization
- Comparison of detection approaches

### 5. Data Management and Reports
- Dataset inspection and preprocessing
- Missing value and duplicate analysis
- Statistical summaries
- Processed CSV exports
- Downloadable PDF analytics reports

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Web Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Statistical Analysis | SciPy |
| Machine Learning | Scikit-learn |
| Data Visualization | Plotly |
| Reporting | ReportLab |
| Development Environment | VS Code |
| Version Control | Git and GitHub |

## 📊 Dataset

CyberWatch uses the UNSW-NB15 cybersecurity dataset.

Official dataset:
https://research.unsw.edu.au/projects/unsw-nb15-dataset

Dataset partitions:

- Training set: 175,341 records
- Testing set: 82,332 records

Download these files:

- UNSW_NB15_training-set.csv
- UNSW_NB15_testing-set.csv

Place both files inside:

data/raw/

The datasets are excluded from the GitHub repository
and must be downloaded separately.

## 🧠 Detection Methodology

### Statistical Threshold-Based Detection

The baseline detector examines three traffic features:

- Source bytes
- Connection duration
- Traffic rate

Thresholds are calculated using the 99th percentile
of normal-labeled training records.

Events exceeding one or more thresholds are flagged
as potentially suspicious.

### Decision Tree Classification

A supervised Decision Tree classifier is trained using
network traffic features, including:

- Connection duration
- Source and destination bytes
- Packet counts
- Traffic rate
- Protocol
- Network service
- Connection state

The classifier is evaluated using the separate
UNSW-NB15 testing partition.

## 📈 Evaluation Results

| Metric | Statistical Rules | Decision Tree |
|---|---:|---:|
| Accuracy | 46.34% | 88.38% |
| Precision | 68.80% | 96.94% |
| Recall | 4.65% | 81.47% |
| F1-Score | 8.71% | 88.53% |

The Decision Tree demonstrated higher performance
than the statistical baseline on the testing dataset.

These results represent performance on the UNSW-NB15
benchmark and do not establish reliability in
real-world production environments.

## ⚙️ Installation

### 1. Clone the repository

git clone https://github.com/Monika-mls/CyberWatch.git

cd CyberWatch-BDA

### 2. Create a virtual environment

python -m venv .venv

### 3. Activate the environment

Windows PowerShell:

.\.venv\Scripts\Activate.ps1

### 4. Install dependencies

python -m pip install -r requirements.txt

### 5. Download the dataset

Download the training and testing CSV files
and place them inside data/raw/.

### 6. Run CyberWatch

python -m streamlit run main.py

Open the local address displayed in the terminal.

## 🔄 Project Workflow

Data Collection
    ↓
Data Preprocessing
    ↓
Statistical Analysis
    ↓
Threat Detection
    ↓
Event Stream Simulation
    ↓
Interactive Visualization
    ↓
Detection Evaluation
    ↓
Security Reports

## 📚 BDA Syllabus Relevance

### Unit I: Data Management
- Data collection and preprocessing
- Data types and data sources
- Dataset exploration

### Unit II: Statistical Analysis
- Descriptive statistics
- Percentiles and distributions
- Statistical threshold detection

### Unit III: Mining Data Streams
- Simulated event streaming
- Stream sampling
- Filtering suspicious events

### Unit V: Data Visualization and Ethics
- Interactive security dashboards
- Visual interpretation of results
- Responsible use of cybersecurity data

Hadoop, HDFS, MapReduce, Hive, and Pig are not
implemented in the current application.

## ⚠️ Limitations

- Live monitoring is simulated using historical data.
- The statistical detector has limited attack recall.
- The Decision Tree is evaluated on a benchmark dataset.
- Real network packet capture is not implemented.
- The system is not a production security solution.

## 🔮 Future Scope

- Apache Kafka-based event streaming
- Hadoop and Spark integration
- Additional classification algorithms
- Real-time network log ingestion
- Advanced anomaly detection
- Automated incident investigation

## 📌 Project Information

Course: Big Data Analytics

Project Type: Course-Based Project

Project Title: CyberWatch - Stream-Based Cybersecurity
Threat Analytics and Visualization Platform
