import sys
import os
sys.path.append(os.path.abspath('..'))

import numpy as np
import pandas as pd
import pickle
import pytest

# ── Load data and model once for all tests ──────────────────────
@pytest.fixture(scope='module')
def data():
    df = pd.read_csv('../data/processed/train_final.csv')
    return df

@pytest.fixture(scope='module')
def model():
    with open('../models/rf_optimised.pkl', 'rb') as f:
        return pickle.load(f)

@pytest.fixture(scope='module')
def features(data):
    feature_cols = [col for col in data.columns if col not in ['unit_id', 'cycle', 'RUL']]
    return data[feature_cols]

# ── Data Tests ───────────────────────────────────────────────────
def test_data_shape(data):
    assert data.shape[0] > 0, "Dataset is empty"
    assert data.shape[1] == 21, "Expected 21 columns"

def test_no_missing_values(data):
    assert data.isnull().sum().sum() == 0, "Missing values found"

def test_rul_column_exists(data):
    assert 'RUL' in data.columns, "RUL column missing"

def test_rul_non_negative(data):
    assert (data['RUL'] >= 0).all(), "Negative RUL values found"

def test_sensor11_exists(data):
    assert 'sensor_11' in data.columns, "sensor_11 column missing"

# ── Model Tests ──────────────────────────────────────────────────
def test_model_loads(model):
    assert model is not None, "Model failed to load"

def test_model_type(model):
    from sklearn.ensemble import RandomForestRegressor
    assert isinstance(model, RandomForestRegressor), "Wrong model type"

def test_model_prediction_shape(model, features):
    preds = model.predict(features.head(10))
    assert preds.shape == (10,), "Prediction shape mismatch"

def test_model_prediction_non_negative(model, features):
    preds = model.predict(features.head(100))
    assert (preds >= 0).all(), "Negative predictions found"

def test_model_r2_above_threshold(model, features, data):
    from sklearn.metrics import r2_score
    y = data['RUL'].clip(upper=125).values
    X = features.values
    preds = model.predict(X)
    r2 = r2_score(y, preds)
    assert r2 > 0.75, f"R2 below threshold: {r2:.4f}"