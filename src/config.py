"""
Application configuration, constants, and session state initialization.
"""

import os
import streamlit as st

# Streamlit Page Config
PAGE_CONFIG = {
    "page_title": "AgriVision Pro - Clinical Plant Diagnostic Suite",
    "page_icon": "🌿",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Project directories and file paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAINED_DATA_DIR = os.path.join(BASE_DIR, "trained data")
DISEASE_CLASSES_PATH = os.path.join(BASE_DIR, "disease_classes.json")
TOP20_CLASSES_PATH = (
    os.path.join(TRAINED_DATA_DIR, "top20_disease_classes.json")
    if os.path.exists(os.path.join(TRAINED_DATA_DIR, "top20_disease_classes.json"))
    else os.path.join(BASE_DIR, "top20_disease_classes.json")
)
TOP40_CLASSES_PATH = os.path.join(BASE_DIR, "top40_disease_classes.json")

# Sample field images
SAMPLE_IMAGE_CANDIDATES = [
    os.path.join(BASE_DIR, "photo_2026-10-24_01-39-50.png"),
    os.path.join(BASE_DIR, "photo_2026-10-24_16-36-24.jpg")
]

def get_sample_image_path() -> str:
    """Returns the first available sample image path."""
    for path in SAMPLE_IMAGE_CANDIDATES:
        if os.path.exists(path):
            return path
    return SAMPLE_IMAGE_CANDIDATES[0]

def init_session_state():
    """Initializes Streamlit session state variables with default values."""
    defaults = {
        "logged_in": False,
        "user_email": "",
        "user_name": "",
        "user_role": "",
        "user_avatar": "",
        "oauth_error": "",
        "active_sample_loaded": False,
        "seg_view_selector": "SAM 2 Pixel Mask"
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
