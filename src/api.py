import sys
import os
sys.path.append(os.path.abspath('..'))

import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'models', 'rf_optimised.pkl'), 'rb') as f:
    rf_model = pickle.load(f)

with open(os.path.join(BASE_DIR, 'models', 'iso_forest.pkl'), 'rb') as f:
    iso_model = pickle.load(f)

# ── FastAPI app ──────────────────────────────────────────────────
app = FastAPI(
    title="PredictiveSense AI — API",
    description="REST API for RUL Prediction & Anomaly Detection",
    version="1.0.0"
)

# ── Input schema ─────────────────────────────────────────────────
class SensorInput(BaseModel):
    # 18 sensor features (same order as training data)
    features: List[float]

# ── Routes ───────────────────────────────────────────────────────
@app.get("/")
def home():
    return {
        "project": "PredictiveSense AI",
        "version": "1.0.0",
        "endpoints": ["/predict/rul", "/predict/anomaly", "/health"]
    }

@app.get("/health")
def health():
    return {"status": "OK", "models_loaded": True}

@app.post("/predict/rul")
def predict_rul(data: SensorInput):
    if len(data.features) != 18:
        raise HTTPException(status_code=400, 
            detail=f"Expected 18 features, got {len(data.features)}")
    
    X = np.array(data.features).reshape(1, -1)
    rul = rf_model.predict(X)[0]
    rul = max(0, round(float(rul), 2))
    
    # Alert status based on RUL
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
    if len(data.features) != 15:
        raise HTTPException(status_code=400,
            detail=f"Expected 15 features, got {len(data.features)}")
    
    X = np.array(data.features).reshape(1, -1)
    result = iso_model.predict(X)[0]
    score  = iso_model.decision_function(X)[0]
    
    return {
        "anomaly_detected": bool(result == -1),
        "anomaly_score": round(float(score), 4),
        "label": "ANOMALY" if result == -1 else "NORMAL"
    }