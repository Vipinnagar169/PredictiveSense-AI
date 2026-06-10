# 🚀 PredictiveSense AI
### AI-Powered Predictive Sensor Monitoring & Failure Detection Platform

![Python](https://img.shields.io/badge/Python-3.14-blue)
![ML](https://img.shields.io/badge/ML-RandomForest-green)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange)
![Internship](https://img.shields.io/badge/DRDO-Internship%202026-red)

---

## 📌 Project Overview
PredictiveSense AI is an end-to-end machine learning platform that monitors 
multivariate sensor data from industrial and defence-grade equipment to:
- 🔍 Detect anomalies in real-time sensor readings
- 📊 Predict Remaining Useful Life (RUL) of critical components
- 🚨 Generate early warning alerts before equipment failure
- 📈 Visualize sensor health trends on an interactive dashboard

> **DRDO Relevance:** Directly applicable to health monitoring of defence 
> vehicles, aircraft engines, and mission-critical equipment.

---

## 📊 Dataset
**NASA C-MAPSS Turbofan Engine Degradation Dataset**
- 100 engines monitored from start to failure
- 20,631 sensor readings
- 26 sensor channels
- Source: [Kaggle - NASA C-MAPSS](https://www.kaggle.com/datasets/behrad3d/nasa-cmaps)

---

## 🏗️ Project Structure

PredictiveSense-AI/
├── data/
│   ├── raw/              # NASA C-MAPSS raw dataset
│   └── processed/        # Cleaned & ML-ready data
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   ├── 04_model_improvement.ipynb
│   └── 05_anomaly_detection.ipynb
├── models/               # Saved ML models
├── src/                  # Python scripts
├── dashboard/            # Streamlit app (upcoming)
├── .gitignore
├── requirements.txt
└── README.md

---

## ⚙️ Tech Stack
| Technology | Purpose |
|------------|---------|
| Python 3.14 | Core language |
| Pandas & NumPy | Data manipulation |
| Matplotlib | Visualization |
| Scikit-learn | ML models & preprocessing |
| Streamlit | Interactive dashboard (upcoming) |

---

## 📈 Results So Far
| Metric | Baseline | Improved |
|--------|----------|----------|
| R2 Score | 0.62 | **0.79** |
| RMSE | 41.47 cycles | **18.66 cycles** |
| MAE | 29.63 cycles | **13.39 cycles** |
| Improvement | — | **55% better** |

**Key Finding:** Sensor 11 is the most critical failure indicator (40% feature importance)

---

## 🔍 Anomaly Detection
- Algorithm: Isolation Forest
- Anomalies Detected: **1,032 out of 20,631 (5%)**
- Finding: Anomaly concentration peaks near failure zone (RUL < 50)

---

## 🚀 How to Run
```bash
# Clone the repository
git clone https://github.com/Vipinnagar169/PredictiveSense-AI.git

# Install dependencies
pip install -r requirements.txt

# Open notebooks in order
# 01 → 02 → 03 → 04 → 05
```

---

## 📅 Progress
- [x] Day 1 — Environment Setup
- [x] Day 2 — Exploratory Data Analysis
- [x] Day 3 — Feature Engineering
- [x] Day 4 — Random Forest Model Training
- [x] Day 5 — Model Improvement (55%)
- [x] Day 6 — Anomaly Detection
- [x] Day 7 — GitHub Setup
- [x] Day 8 — README Documentation
- [ ] Day 9+ — LSTM Deep Learning
- [ ] Streamlit Dashboard
- [ ] Final Presentation

---

## 👨‍💻 Author
**Vipin Nagar**  
Pre-Final Year B.E. (Information Technology)  
DRDO Internship 2026  

---
*Project developed during 45-day DRDO Internship (June–July 2026)*