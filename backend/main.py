"""
AgriVision Pro - FastAPI Web Server & SPA Host.
Serves the studio-grade clinical web interface, dedicated login page, and multimodal AI REST API.
"""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.config import BASE_DIR
from backend.routes import auth, diagnosis, voice, report, benchmark

app = FastAPI(
    title="AgriVision Pro - Clinical Plant Diagnostic Suite",
    description="Multimodal Deep-Learning Agronomic Diagnostic & Decision Support API",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def disable_static_cache(request: Request, call_next):
    """Ensures browser always loads the latest HTML/JS/CSS without stale 304 cache."""
    response = await call_next(request)
    if request.url.path in ("/", "/login") or request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


# Register API routers
app.include_router(auth.router)
app.include_router(diagnosis.router)
app.include_router(voice.router)
app.include_router(report.router)
app.include_router(benchmark.router)

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Mount frontend static assets (/static/css, /static/js)
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/login")
def serve_login_page():
    """Serves the dedicated standalone Clinical Login Page."""
    login_path = os.path.join(FRONTEND_DIR, "login.html")
    return FileResponse(login_path)


@app.get("/")
def serve_spa_index():
    """Serves the main Single-Page Application (SPA) HTML shell."""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    return FileResponse(index_path)
