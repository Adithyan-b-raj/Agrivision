# 🌿 AgriVision Pro: Complete Installation & Workstation Setup Guide
### Step-by-Step Environment Preparation for Windows, macOS, and Linux
**Department of Computer Science & Engineering • St. Thomas Institute for Science & Technology (STIST)**

---

## 📑 Table of Contents
1. [Prerequisites & System Requirements](#1-prerequisites--system-requirements)
2. [Step 1: Clone Repository with Git LFS](#step-1-clone-repository-with-git-lfs-critical)
3. [Step 2: Create & Activate Virtual Environment](#step-2-create--activate-virtual-environment)
4. [Step 3: Install Dependencies](#step-3-install-dependencies)
5. [Step 4: Configure Environment Keys (.env)](#step-4-configure-environment-keys-env)
6. [Step 5: Launch the Application](#step-5-launch-the-application)
7. [Default Login Credentials](#7-default-login-credentials)
8. [Troubleshooting & Common Issues](#8-troubleshooting--common-issues)

---

## 1. Prerequisites & System Requirements

Before you begin, verify that the target machine has the following tools installed:

| Component | Minimum Requirement | Recommended |
| :--- | :--- | :--- |
| **Python** | Python 3.10.x | Python 3.10, 3.11, or 3.12 |
| **Git & Git LFS** | Git 2.30+ with Git LFS | Latest Git + Git LFS 3.x |
| **RAM** | 8 GB System Memory | 16 GB System Memory |
| **Storage** | 3.5 GB free disk space | 5+ GB SSD space |
| **GPU (Optional)** | CPU-only supported (14.2 ms) | NVIDIA GPU (GTX 1650 / RTX / Tesla) with CUDA 11.8+ or 12.1+ |

---

## Step 1: Clone Repository with Git LFS (Critical)

> [!IMPORTANT]
> The trained deep learning checkpoints (`.pth`, `.pt` files totaling ~322 MB) are tracked using **Git LFS (Large File Storage)**. If Git LFS is not installed before cloning, Git will only download text pointer files, causing PyTorch to throw an `EOFError: Ran out of input`.

### 1. Install Git LFS
- **Windows**: Included with the official [Git for Windows installer](https://git-scm.com/download/win).
- **macOS**: `brew install git-lfs`
- **Linux (Ubuntu/Debian)**: `sudo apt install git-lfs`

### 2. Initialize Git LFS & Clone
Open your terminal or PowerShell and run:

```bash
# Initialize Git LFS on the machine
git lfs install

# Clone the repository
git clone https://github.com/Adithyan-b-raj/Agrivision.git
cd Agrivision

# Ensure all large model checkpoints are completely downloaded
git lfs pull
```

---

## Step 2: Create & Activate Virtual Environment

Always use an isolated virtual environment to prevent package version conflicts:

### On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If you see an execution policy error on PowerShell, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once).*

### On Windows (Command Prompt `cmd`):
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### On macOS / Linux (Bash or Zsh):
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Dependencies

### Option A: Standard CPU Installation (Default)
Run the following command inside the project directory:

```bash
pip install -r requirements.txt
```

Or install all core packages directly via a single command:
```bash
pip install fastapi uvicorn python-multipart streamlit torch torchvision timm ultralytics opencv-python-headless pillow numpy gTTS deep-translator fpdf2 python-dotenv google-auth google-auth-oauthlib requests
```

---

### Option B: NVIDIA GPU Acceleration (CUDA)
If the machine has a dedicated NVIDIA GPU and you want CUDA hardware acceleration:

```bash
# 1. Install PyTorch with CUDA 12.1 runtime
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# 2. Install remaining dependencies
pip install -r requirements.txt
```

Verify GPU availability:
```bash
python -c "import torch; print('CUDA Available:', torch.cuda.is_available(), '| Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

---

## Step 4: Configure Environment Keys (.env)

Create a local `.env` configuration file in the project root:

### Windows:
```powershell
copy .env.example .env
```

### macOS / Linux:
```bash
cp .env.example .env
```

### Edit `.env`
Open the `.env` file in any text editor. It should look like this:

```env
# Google OAuth 2.0 Configuration (Optional for Google SSO)
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/

# Clinical Workstation Authorized Credentials (Works Out-of-the-Box)
CLINICAL_USERNAME=agronomist
CLINICAL_EMAIL=agronomist.evaluator@agrivision.ai
CLINICAL_PASSWORD=AgriVision2026
CLINICAL_NAME=Dr. Agronomist Evaluator
CLINICAL_ROLE=Senior Plant Pathologist • STIST Lab
```

> [!NOTE]
> Changes saved to `.env` are **hot-reloaded dynamically** by the FastAPI backend—you do not need to restart the server when changing credentials.

---

## Step 5: Launch the Application

AgriVision Pro provides two independent interfaces:

### 1. Primary Workstation: FastAPI + Studio Web SPA (Recommended)
```bash
python run.py
```
- 🌐 **Web Diagnostic Suite**: [http://localhost:8000](http://localhost:8000)
- 🔒 **Dedicated Login Portal**: [http://localhost:8000/login](http://localhost:8000/login)
- 📘 **Interactive OpenAPI Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Secondary Workstation: Streamlit Diagnostic Dashboard
```bash
streamlit run app.py
```
- 🌐 **Streamlit UI**: [http://localhost:8501](http://localhost:8501)

---

## 7. Default Login Credentials

You can sign into the Clinical Workstation using the following pre-configured credentials:

| Field | Default Value | Notes |
| :--- | :--- | :--- |
| **Username or Email** | `agronomist` *or* `agronomist.evaluator@agrivision.ai` | Configured via `CLINICAL_USERNAME` / `CLINICAL_EMAIL` |
| **Workstation Password** | `AgriVision2026` | Configured via `CLINICAL_PASSWORD` in `.env` |
| **Clinician Name** | `Dr. Agronomist Evaluator` | Synchronized with PDF report header |
| **Clinical Role** | `Senior Plant Pathologist • STIST Lab` | Institutional affiliation |

---

## 8. Troubleshooting & Common Issues

### 1. PyTorch throws `EOFError: Ran out of input` or `PytorchStreamReader failed reading zip archive`
- **Cause**: Git LFS was not initialized before cloning, and only 130-byte pointer files were downloaded.
- **Fix**: Run `git lfs install` followed by `git lfs pull` inside the repository root.

### 2. Port 8000 is already in use
- **Windows**:
  ```powershell
  Get-NetTCPConnection -LocalPort 8000 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
  ```
- **macOS / Linux**:
  ```bash
  kill -9 $(lsof -t -i:8000)
  ```

### 3. Google OAuth Redirect URI Mismatch (`redirect_uri_mismatch`)
- In [Google Cloud Console](https://console.cloud.google.com/apis/credentials), ensure that **Authorized redirect URIs** includes `http://localhost:8000` (without trailing slash) for FastAPI, or `http://localhost:8501` for Streamlit.
- Match `GOOGLE_REDIRECT_URI=http://localhost:8000` in your `.env`.

### 4. Windows PowerShell Script Execution Policy Error
If running `.\venv\Scripts\Activate.ps1` gives an authorization error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 5. Quick Terminal Smoke Test
Verify that the full 3-stage model cascade loads cleanly:
```bash
python -c "from src.models.loaders import load_trained_convnext_model, load_rtdetr_model, load_sam2_model; m, c = load_trained_convnext_model(); r, n = load_rtdetr_model(); s = load_sam2_model(); print('✅ ConvNeXt:', len(c), 'classes | RT-DETR:', n, '| SAM 2.1:', s is not None)"
```
**Expected Output:**
```text
✅ ConvNeXt: 20 classes | RT-DETR: best_rtdetr_leaf_disease.pt | SAM 2.1: True
```

---

*Authored by AgriVision Pro Engineering Team • STIST Trivandrum (2026).*
