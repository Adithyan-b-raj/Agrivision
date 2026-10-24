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

:: 2. Check and pull Git LFS model checkpoints
echo [*] Checking AI model weights...
git lfs version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [*] Syncing large model files via Git LFS...
    git lfs pull
) else (
    echo [!] Git LFS not detected in PATH. Checking local model files...
)

:: Verify model file size (must be real weights > 10 MB, not 130-byte pointer)
if exist "trained data\best_convnextv2_top20.pth" (
    for %%F in ("trained data\best_convnextv2_top20.pth") do set "FILE_SIZE=%%~zF"
    if !FILE_SIZE! LSS 10000000 (
        echo.
        echo [WARNING] Model file appears to be a Git LFS text pointer (!FILE_SIZE! bytes).
        echo If you downloaded this repository as a ZIP from GitHub:
        echo GitHub ZIP downloads do not include Git LFS files.
        echo Please install Git LFS (https://git-lfs.com) and run:
        echo   git lfs pull
        echo.
    ) else (
        echo [*] Deep learning weights verified (!FILE_SIZE! bytes).
    )
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

:: 6. Launch Application and open browser
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
