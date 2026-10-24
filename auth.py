"""
Google OAuth 2.0 Authentication Module for AgriVision AI
Credentials are read strictly from environment keys (.env / os.environ / st.secrets).
No credentials entry or secret management is required in the frontend.
"""

import os
import urllib.parse
import requests
import streamlit as st
from dotenv import load_dotenv

# Automatically load environment variables from .env file
load_dotenv()

DEFAULT_REDIRECT_URI = "http://localhost:8501"

def load_oauth_credentials():
    """
    Loads Google OAuth 2.0 credentials from environment variables / .env,
    with fallback to st.secrets.
    Returns: (client_id, client_secret, redirect_uri)
    """
    # 1. Environment variables (.env or system env)
    client_id = os.environ.get("GOOGLE_CLIENT_ID", "").strip()
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "").strip()
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", DEFAULT_REDIRECT_URI).strip()

    # 2. Fallback to st.secrets if not set in os.environ
    if not client_id or not client_secret:
        try:
            if hasattr(st, "secrets"):
                if "GOOGLE_CLIENT_ID" in st.secrets:
                    client_id = client_id or st.secrets["GOOGLE_CLIENT_ID"].strip()
                if "GOOGLE_CLIENT_SECRET" in st.secrets:
                    client_secret = client_secret or st.secrets["GOOGLE_CLIENT_SECRET"].strip()
                if "google_client_id" in st.secrets:
                    client_id = client_id or st.secrets["google_client_id"].strip()
                if "google_client_secret" in st.secrets:
                    client_secret = client_secret or st.secrets["google_client_secret"].strip()
                if "google" in st.secrets:
                    client_id = client_id or st.secrets["google"].get("client_id", "").strip()
                    client_secret = client_secret or st.secrets["google"].get("client_secret", "").strip()
                if "GOOGLE_REDIRECT_URI" in st.secrets:
                    redirect_uri = st.secrets["GOOGLE_REDIRECT_URI"].strip()
                elif "redirect_uri" in st.secrets:
                    redirect_uri = st.secrets["redirect_uri"].strip()
        except Exception:
            pass

    return client_id, client_secret, redirect_uri or DEFAULT_REDIRECT_URI


def get_google_auth_url(client_id: str, redirect_uri: str, state: str = "agrivision_oauth") -> str:
    """
    Constructs the official Google OAuth 2.0 authorization URL.
    """
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
        "state": state
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"


def exchange_code_for_user_info(code: str, client_id: str, client_secret: str, redirect_uri: str):
    """
    Exchanges authorization code for Google access token, then retrieves user profile.
    Returns: (success: bool, data_or_error: dict|str)
    """
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    headers = {
        "Accept": "application/json"
    }

    try:
        token_resp = requests.post(token_url, data=payload, headers=headers, timeout=12)
        token_json = token_resp.json()

        if token_resp.status_code != 200 or "access_token" not in token_json:
            error_msg = token_json.get("error_description", token_json.get("error", "Unknown token error"))
            return False, f"Google token exchange failed ({token_resp.status_code}): {error_msg}"

        access_token = token_json["access_token"]
        
        # Request user profile info from Google UserInfo endpoint
        userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        user_resp = requests.get(
            userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=12
        )
        
        if user_resp.status_code != 200:
            return False, f"Failed to fetch user profile from Google ({user_resp.status_code}): {user_resp.text}"

        user_info = user_resp.json()
        return True, user_info

    except requests.exceptions.RequestException as e:
        return False, f"Network communication error with Google OAuth servers: {str(e)}"
    except Exception as e:
        return False, f"Authentication exception: {str(e)}"
