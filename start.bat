@echo off
title AgriVision Pro - Auto Setup & Launch
echo ============================================================
echo   🌿 AgriVision Pro: Automated Setup & Workstation Launch
echo ============================================================
echo.

:: 1. Ensure Git LFS model weights are pulled
echo [*] Checking model weights (Git LFS)...
git lfs pull >nul 2>&1

:: 2. Setup .env file if missing
if not exist .env (
    echo [*] Creating .env from .env.example...
    copy .env.example .env >nul
)

:: 3. Setup Python Virtual Environment if missing
if not exist venv (
    echo [*] Creating virtual environment (venv)...
    python -m venv venv
)

:: 4. Install / Update Dependencies
echo [*] Installing required packages...
.\venv\Scripts\python.exe -m pip install -r requirements.txt

:: 5. Launch FastAPI Application
echo.
echo ============================================================
echo   🚀 Launching AgriVision Pro at http://localhost:8000
echo ============================================================
echo.
.\venv\Scripts\python.exe run.py
pause
