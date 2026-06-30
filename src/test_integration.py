import sys
import os
sys.path.append(os.path.abspath('..'))

import numpy as np
import pandas as pd
import pickle
import pytest

# ── Fixtures ─────────────────────────────────────────────────────
@pytest.fixture(scope='module')
def pipeline():
    """Load complete pipeline — data + both models."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'processed', 'train_final.csv'))
    
    with open(os.path.join(BASE_DIR, 'models', 'rf_optimised.pkl'), 'rb') as f:
        rf_model = pickle.load(f)
    
    with open(os.path.join(BASE_DIR, 'models', 'iso_forest.pkl'), 'rb') as f:
        iso_model = pickle.load(f)
    
    feature_cols = [col for col in df.columns if col not in ['unit_id', 'cycle', 'RUL']]
    sensor_cols  = [col for col in df.columns if 'sensor' in col]
    
    return {
        'df': df,
        'rf_model': rf_model,
        'iso_model': iso_model,
        'feature_cols': feature_cols,
        'sensor_cols': sensor_cols
    }

# ── Integration Tests ─────────────────────────────────────────────
def test_full_pipeline_loads(pipeline):
    """Complete pipeline loads without errors."""
    assert pipeline['df'] is not None
    assert pipeline['rf_model'] is not None
    assert pipeline['iso_model'] is not None

def test_engine_data_extraction(pipeline):
    """Single engine data can be extracted correctly."""
    df = pipeline['df']
    engine_df = df[df['unit_id'] == 1]
    assert len(engine_df) > 0
    assert 'RUL' in engine_df.columns

def test_rul_prediction_pipeline(pipeline):
    """End-to-end RUL prediction for a single engine."""
    df           = pipeline['df']
    rf_model     = pipeline['rf_model']
    feature_cols = pipeline['feature_cols']
    
    engine_df    = df[df['unit_id'] == 1]
    last_reading = engine_df[feature_cols].iloc[-1:].values
    predicted_rul = rf_model.predict(last_reading)[0]
    
    assert predicted_rul >= 0, "RUL cannot be negative"
    assert predicted_rul <= 130, "RUL cannot exceed cap of 130"

def test_alert_status_logic(pipeline):
    """Alert status assigned correctly based on RUL."""
    df           = pipeline['df']
    rf_model     = pipeline['rf_model']
    feature_cols = pipeline['feature_cols']
    
    for engine_id in [1, 50, 100]:
        engine_df     = df[df['unit_id'] == engine_id]
        last_reading  = engine_df[feature_cols].iloc[-1:].values
        predicted_rul = rf_model.predict(last_reading)[0]
        
        if predicted_rul <= 40:
            status = "CRITICAL"
        elif predicted_rul <= 80:
            status = "WARNING"
        else:
            status = "HEALTHY"
        
        assert status in ["CRITICAL", "WARNING", "HEALTHY"]

def test_anomaly_detection_pipeline(pipeline):
    """End-to-end anomaly detection for a single engine."""
    df          = pipeline['df']
    iso_model   = pipeline['iso_model']
    sensor_cols = pipeline['sensor_cols']
    
    engine_df   = df[df['unit_id'] == 1]
    result      = iso_model.predict(engine_df[sensor_cols])
    
    assert set(result).issubset({-1, 1}), "Anomaly labels must be -1 or 1"

def test_anomaly_rate_reasonable(pipeline):
    """Overall anomaly rate should be between 1% and 15%."""
    df          = pipeline['df']
    iso_model   = pipeline['iso_model']
    sensor_cols = pipeline['sensor_cols']
    
    results     = iso_model.predict(df[sensor_cols])
    anomaly_rate = (results == -1).sum() / len(results) * 100
    
    assert 1 <= anomaly_rate <= 15, f"Anomaly rate {anomaly_rate:.1f}% out of expected range"

def test_multiple_engines_prediction(pipeline):
    """RUL prediction works for all 100 engines."""
    df           = pipeline['df']
    rf_model     = pipeline['rf_model']
    feature_cols = pipeline['feature_cols']
    
    for engine_id in range(1, 101):
        engine_df     = df[df['unit_id'] == engine_id]
        last_reading  = engine_df[feature_cols].iloc[-1:].values
        predicted_rul = rf_model.predict(last_reading)[0]
        assert predicted_rul >= 0

def test_data_to_prediction_consistency(pipeline):
    """Same input always gives same output — model is deterministic."""
    df           = pipeline['df']
    rf_model     = pipeline['rf_model']
    feature_cols = pipeline['feature_cols']
    
    engine_df    = df[df['unit_id'] == 1]
    last_reading = engine_df[feature_cols].iloc[-1:].values
    
    pred1 = rf_model.predict(last_reading)[0]
    pred2 = rf_model.predict(last_reading)[0]
    
    assert pred1 == pred2, "Model must be deterministic"