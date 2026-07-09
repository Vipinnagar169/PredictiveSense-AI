@echo off
title PredictiveSense AI — Launcher
color 1F

echo.
echo  ========================================
echo   PredictiveSense AI - DRDO Internship
echo   AI-Powered Predictive Sensor Monitor
echo  ========================================
echo.

cd /d "%~dp0"

echo  Installing dependencies...
python -m pip install -r requirements.txt --quiet

echo.
echo  Starting Dashboard...
echo.

python -m streamlit run dashboard/app.py

pause