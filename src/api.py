"""
PredictiveSense AI — FastAPI REST API
======================================
REST API for RUL Prediction & Anomaly Detection
DRDO Internship 2026 | Vipin Nagar
GitHub: github.com/Vipinnagar169/PredictiveSense-AI

Endpoints:
    GET  /              — API info and available endpoints
    GET  /health        — API health check
    POST /predict/rul   — Predict Remaining Useful Life (18 features)
    POST /predict/anomaly — Detect anomaly in sensor readings (15 features)

Run:
    uvicorn src.api:app --reload
    Access at: http://127.0.0.1:8000
"""

import sys
import os
sys.path.append(os.path.abspath('..'))

import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# ── Load Models ───────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'models', 'rf_optimised.pkl'), 'rb') as f:
    rf_model = pickle.load(f)

with open(os.path.join(BASE_DIR, 'models', 'iso_forest.pkl'), 'rb') as f:
    iso_model = pickle.load(f)

# ── FastAPI App ───────────────────────────────────────────────────
app = FastAPI(
    title="PredictiveSense AI — API",
    description="REST API for RUL Prediction & Anomaly Detection | DRDO Internship 2026",
    version="1.0.0"
)

# ── Input Schema ──────────────────────────────────────────────────
class SensorInput(BaseModel):
    """
    Input schema for sensor feature data.
    
    Attributes:
        features (List[float]): List of normalised sensor readings.
            - For /predict/rul      : 18 features required
            - For /predict/anomaly  : 15 features required
            Features must be in the same order as training data.
    """
    features: List[float]

# ── Routes ────────────────────────────────────────────────────────
@app.get("/")
def home():
    """
    Root endpoint — returns API info and available endpoints.
    
    Returns:
        dict: Project name, version, and list of endpoints.
    """
    return {
        "project": "PredictiveSense AI",
        "version": "1.0.0",
        "endpoints": ["/predict/rul", "/predict/anomaly", "/health"]
    }


@app.get("/health")
def health():
    """
    Health check endpoint — verifies API and models are running.
    
    Returns:
        dict: API status and model load confirmation.
    """
    return {"status": "OK", "models_loaded": True}


@app.post("/predict/rul")
def predict_rul(data: SensorInput):
    """
    Predict Remaining Useful Life (RUL) for an engine.
    
    Uses the optimised Random Forest model (rf_optimised.pkl)
    trained on NASA C-MAPSS turbofan engine data.
    
    Alert thresholds:
        - CRITICAL : RUL <= 40 cycles
        - WARNING  : RUL <= 80 cycles
        - HEALTHY  : RUL >  80 cycles
    
    Args:
        data (SensorInput): 18 normalised sensor feature values.
    
    Returns:
        dict: predicted_rul (float), status (str), unit (str)
    
    Raises:
        HTTPException 400: If number of features != 18
    """
    if len(data.features) != 18:
        raise HTTPException(status_code=400,
            detail=f"Expected 18 features, got {len(data.features)}")

    X   = np.array(data.features).reshape(1, -1)
    rul = max(0, round(float(rf_model.predict(X)[0]), 2))

    if rul <= 40:
        status = "CRITICAL"
    elif rul <= 80:
        status = "WARNING"
    else:
        status = "HEALTHY"

    return {
        "predicted_rul": rul,
        "status": status,
        "unit": "cycles"
    }


@app.post("/predict/anomaly")
def predict_anomaly(data: SensorInput):
    """
    Detect anomaly in engine sensor readings.
    
    Uses the Isolation Forest model (iso_forest.pkl) trained
    with contamination=0.05 (5% expected anomalies).
    
    Args:
        data (SensorInput): 15 normalised sensor feature values.
    
    Returns:
        dict:
            - anomaly_detected (bool): True if anomaly found
            - anomaly_score (float): Isolation Forest decision score
                                     (negative = anomaly, positive = normal)
            - label (str): 'ANOMALY' or 'NORMAL'
    
    Raises:
        HTTPException 400: If number of features != 15
    """
    if len(data.features) != 15:
        raise HTTPException(status_code=400,
            detail=f"Expected 15 features, got {len(data.features)}")

    X      = np.array(data.features).reshape(1, -1)
    result = iso_model.predict(X)[0]
    score  = iso_model.decision_function(X)[0]

    return {
        "anomaly_detected": bool(result == -1),
        "anomaly_score": round(float(score), 4),
        "label": "ANOMALY" if result == -1 else "NORMAL"
    }