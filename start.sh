#!/usr/bin/env bash
set -e

echo "============================================================"
echo "  🌿 AgriVision Pro: Automated Setup & Workstation Launch"
echo "============================================================"
echo ""

# 1. Ensure Git LFS model weights are pulled
echo "[*] Checking model weights (Git LFS)..."
git lfs pull 2>/dev/null || true

# 2. Setup .env file if missing
if [ ! -f .env ]; then
    echo "[*] Creating .env from .env.example..."
    cp .env.example .env
fi

# 3. Setup Python Virtual Environment if missing
if [ ! -d venv ]; then
    echo "[*] Creating virtual environment (venv)..."
    python3 -m venv venv
fi

# 4. Install / Update Dependencies
echo "[*] Installing required packages..."
./venv/bin/pip install -r requirements.txt

# 5. Launch FastAPI Application
echo ""
echo "============================================================"
echo "  🚀 Launching AgriVision Pro at http://localhost:8000"
echo "============================================================"
echo ""
./venv/bin/python run.py
