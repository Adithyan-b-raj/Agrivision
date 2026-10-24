#!/usr/bin/env bash
set -e

echo "============================================================"
echo "  🌿 AgriVision Pro: Automated Setup & Workstation Launch"
echo "============================================================"
echo ""

# 1. Check Python installation
PY_CMD=""
if command -v python3 &>/dev/null; then
    PY_CMD="python3"
elif command -v python &>/dev/null; then
    PY_CMD="python"
else
    echo "[ERROR] Python 3.10+ was not found on this system!"
    echo "Please install Python 3.10+ and add it to your PATH."
    exit 1
fi
echo "[*] Detected Python: $($PY_CMD --version)"

# 2. Check and pull Git LFS model weights
echo "[*] Checking AI model weights..."
if command -v git-lfs &>/dev/null || command -v git &>/dev/null; then
    git lfs pull 2>/dev/null || true
fi

if [ -f "trained data/best_convnextv2_top20.pth" ]; then
    FILE_SIZE=$(wc -c < "trained data/best_convnextv2_top20.pth" 2>/dev/null || echo "0")
    if [ "$FILE_SIZE" -lt 10000000 ]; then
        echo ""
        echo "[WARNING] Model file appears to be a Git LFS text pointer ($FILE_SIZE bytes)."
        echo "If you downloaded as ZIP: install git-lfs and run: git lfs pull"
        echo ""
    else
        echo "[*] Deep learning weights verified ($FILE_SIZE bytes)."
    fi
fi

# 3. Setup .env file if missing
if [ ! -f .env ]; then
    echo "[*] Creating .env from .env.example..."
    cp .env.example .env
fi

# 4. Setup Python Virtual Environment if missing
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment (venv)..."
    $PY_CMD -m venv venv
fi

# 5. Install / Update Dependencies
echo "[*] Installing required packages from requirements.txt..."
./venv/bin/pip install --upgrade pip >/dev/null 2>&1 || true
./venv/bin/pip install -r requirements.txt

# 6. Launch Application and open browser
echo ""
echo "============================================================"
echo "  🚀 Launching AgriVision Pro Workstation"
echo "  🌐 Web UI:       http://localhost:8000"
echo "  🔒 Login Portal: http://localhost:8000/login"
echo "  👤 Default User: agronomist"
echo "  🔑 Default Pass: AgriVision2026"
echo "============================================================"
echo ""

# Open default browser after 3 seconds in background
(sleep 3 && {
    if command -v xdg-open &>/dev/null; then xdg-open http://localhost:8000;
    elif command -v open &>/dev/null; then open http://localhost:8000; fi
}) &

./venv/bin/python run.py
