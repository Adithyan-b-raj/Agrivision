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

# 2. Try Git LFS pull if Git LFS is available
if command -v git-lfs &>/dev/null || command -v git &>/dev/null; then
    git lfs pull 2>/dev/null || true
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

# 6. Auto-download model weights if downloaded as ZIP (Resolves Git LFS pointers automatically)
echo "[*] Verifying deep learning weights (auto-resolves ZIP download pointers if needed)..."
./venv/bin/python -c "from src.models.loaders import load_trained_convnext_model, load_rtdetr_model, load_sam2_model; load_trained_convnext_model(); load_rtdetr_model(); load_sam2_model()"

# 7. Launch Application and open browser
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
