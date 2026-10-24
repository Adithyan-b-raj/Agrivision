@echo off
setlocal enabledelayedexpansion
title AgriVision Pro - Clinical Plant Diagnostic Suite
echo ============================================================
echo   🌿 AgriVision Pro: Automated Setup & Workstation Launch
echo ============================================================
echo.

:: 1. Check Python installation
set "PY_CMD="
python --version >nul 2>&1 && set "PY_CMD=python"
if not defined PY_CMD (
    py -3 --version >nul 2>&1 && set "PY_CMD=py -3"
)

if not defined PY_CMD (
    echo [ERROR] Python 3.10+ was not found on this computer!
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo IMPORTANT: Make sure to check the box:
    echo   "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [*] Detected Python environment: %PY_CMD%

:: 2. Try Git LFS pull if Git LFS is available
git lfs version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [*] Syncing large model files via Git LFS...
    git lfs pull >nul 2>&1
)

:: 3. Setup .env configuration file if missing
if not exist .env (
    echo [*] Initializing .env configuration from template...
    copy .env.example .env >nul
    echo [*] Created .env with default workstation credentials.
) else (
    echo [*] Found existing .env configuration.
)

:: 4. Create virtual environment if missing
if not exist "venv\Scripts\python.exe" (
    echo [*] Creating isolated virtual environment (venv)...
    %PY_CMD% -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [*] Virtual environment created.
) else (
    echo [*] Virtual environment (venv) ready.
)

:: 5. Install / update dependencies
echo [*] Installing and verifying all required packages from requirements.txt...
.\venv\Scripts\python.exe -m pip install --upgrade pip >nul 2>&1
.\venv\Scripts\python.exe -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Failed to install one or more required packages.
    echo Check your internet connection and try running again.
    pause
    exit /b 1
)
echo [*] All dependencies verified successfully!

:: 6. Auto-download model weights if downloaded as ZIP (Resolves Git LFS pointers automatically)
echo [*] Verifying deep learning weights (auto-resolves ZIP download pointers if needed)...
.\venv\Scripts\python.exe -c "from src.models.loaders import load_trained_convnext_model, load_rtdetr_model, load_sam2_model; load_trained_convnext_model(); load_rtdetr_model(); load_sam2_model()"

:: 7. Launch Application and open browser
echo.
echo ============================================================
echo   🚀 Launching AgriVision Pro Workstation
echo   🌐 Web UI:       http://localhost:8000
echo   🔒 Login Portal: http://localhost:8000/login
echo   👤 Default User: agronomist
echo   🔑 Default Pass: AgriVision2026
echo ============================================================
echo.

:: Open default browser after 3 seconds in background
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8000"

:: Start server
.\venv\Scripts\python.exe run.py
pause
