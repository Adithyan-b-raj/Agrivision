"""
Google OAuth 2.0 Credentials and Token Management.
Reads strictly from environment keys (.env / os.environ / st.secrets).
"""

import os
import urllib.parse
import requests
from dotenv import load_dotenv

# Automatically load environment variables from .env file
load_dotenv()

DEFAULT_REDIRECT_URI = "http://localhost:8000"

def load_oauth_credentials(default_redirect: str = None):
    """
    Loads Google OAuth 2.0 credentials from environment variables / .env.
    Calls load_dotenv(override=True) so changes to .env take effect immediately without server restart.
    Normalizes trailing slash on root origin URIs so http://localhost:8000/ matches Google Cloud Console's http://localhost:8000.
    Returns: (client_id, client_secret, redirect_uri)
    """
    load_dotenv(override=True)
    fallback_redirect = (default_redirect or DEFAULT_REDIRECT_URI).rstrip("/")
    client_id = os.environ.get("GOOGLE_CLIENT_ID", "").strip()
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "").strip()
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", fallback_redirect).strip().rstrip("/")

    return client_id, client_secret, redirect_uri or fallback_redirect


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
            timeout=10
        )
        user_json = user_resp.json()

        if user_resp.status_code != 200:
            return False, f"Failed to retrieve user profile ({user_resp.status_code})"

        return True, user_json

    except requests.exceptions.RequestException as e:
        return False, f"Network communication error with Google OAuth servers: {str(e)}"
    except Exception as e:
        return False, f"Authentication exception: {str(e)}"
