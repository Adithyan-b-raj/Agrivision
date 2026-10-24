"""
AgriVision Pro — Studio Web Application Launcher
Starts the FastAPI + Uvicorn server hosting the Luminous Clinical White SPA and Multimodal AI API.
"""

import sys
import uvicorn

# Ensure UTF-8 stdout on Windows terminals
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

if __name__ == "__main__":
    print("\n" + "=" * 68)
    print(" [AgriVision Pro v3.0] Clinical Plant Diagnostic Suite")
    print(" Studio Web UI:  http://localhost:8000")
    print(" OpenAPI Docs:   http://localhost:8000/docs")
    print("=" * 68 + "\n")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
