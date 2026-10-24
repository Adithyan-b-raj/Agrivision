"""
Authentication & Google OAuth 2.0 API Routes.
Supports Google OAuth 2.0 SSO, Clinical Credentials Sign-In, and Evaluator Access.
"""

import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from src.auth.oauth import (
    load_oauth_credentials,
    get_google_auth_url,
    exchange_code_for_user_info
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def load_clinical_credentials() -> dict:
    """
    Loads authorized clinical credentials from .env.
    Refreshes via load_dotenv(override=True) so runtime edits in .env take effect immediately.
    """
    load_dotenv(override=True)
    username = os.environ.get("CLINICAL_USERNAME", os.environ.get("AUTH_USERNAME", "agronomist")).strip()
    email = os.environ.get("CLINICAL_EMAIL", os.environ.get("AUTH_EMAIL", "agronomist.evaluator@agrivision.ai")).strip()
    password = os.environ.get("CLINICAL_PASSWORD", os.environ.get("AUTH_PASSWORD", "AgriVision2026")).strip()
    name = os.environ.get("CLINICAL_NAME", os.environ.get("AUTH_NAME", "Dr. Agronomist Evaluator")).strip()
    role = os.environ.get("CLINICAL_ROLE", "Senior Plant Pathologist • STIST Lab").strip()
    return {
        "username": username,
        "email": email,
        "password": password,
        "name": name,
        "role": role
    }


class OAuthExchangeRequest(BaseModel):
    code: str
    redirect_uri: str | None = None


class CredentialsLoginRequest(BaseModel):
    email: str | None = None
    username: str | None = None
    username_or_email: str | None = None
    password: str
    name: str | None = None


@router.get("/config")
def get_auth_config(request: Request):
    """Returns Google OAuth 2.0 availability and workstation credentials configuration from .env."""
    origin = f"{request.url.scheme}://{request.url.netloc}"
    client_id, client_secret, redirect_uri = load_oauth_credentials(default_redirect=origin)
    configured = bool(client_id and client_secret)
    auth_url = get_google_auth_url(client_id, redirect_uri) if configured else ""
    creds = load_clinical_credentials()
    return {
        "configured": configured,
        "auth_url": auth_url,
        "redirect_uri": redirect_uri,
        "credentials": {
            "username": creds["username"],
            "email": creds["email"],
            "name": creds["name"],
            "default_password": creds["password"]
        }
    }


@router.post("/google-exchange")
def google_oauth_exchange(payload: OAuthExchangeRequest, request: Request):
    """Exchanges Google OAuth 2.0 authorization code for user profile."""
    origin = f"{request.url.scheme}://{request.url.netloc}"
    client_id, client_secret, env_redirect = load_oauth_credentials(default_redirect=origin)
    if not client_id or not client_secret:
        raise HTTPException(
            status_code=400,
            detail="Google OAuth Client ID and Secret are not configured in .env"
        )
    # Always prioritize the exact redirect_uri used to generate the auth URL (env_redirect)
    target_redirect = env_redirect or payload.redirect_uri or origin
    success, res = exchange_code_for_user_info(
        payload.code, client_id, client_secret, target_redirect
    )
    if not success:
        raise HTTPException(status_code=401, detail=str(res))

    return {
        "logged_in": True,
        "user": {
            "email": res.get("email", ""),
            "name": res.get("name", "Google Agronomist"),
            "avatar": res.get("picture", ""),
            "role": "Authenticated Google Agronomist",
            "auth_mode": "google_oauth"
        }
    }


@router.post("/credentials-login")
def clinical_credentials_login(payload: CredentialsLoginRequest):
    """Authenticates a clinician via workstation username/email and password credentials from .env."""
    identifier = (payload.username_or_email or payload.username or payload.email or "").strip()
    password = (payload.password or "").strip()

    if not identifier:
        raise HTTPException(status_code=400, detail="Please enter your clinical username or email.")
    if not password:
        raise HTTPException(status_code=400, detail="Please enter your workstation password.")

    creds = load_clinical_credentials()
    env_user = creds["username"].strip().lower()
    env_email = creds["email"].strip().lower()
    env_pass = creds["password"].strip()

    ident_lower = identifier.lower()

    # 1. Match against .env CLINICAL_USERNAME or CLINICAL_EMAIL
    if ident_lower == env_user or ident_lower == env_email:
        if env_pass and password != env_pass:
            raise HTTPException(status_code=401, detail="Incorrect password for this workstation account.")
        
        display_name = (payload.name and payload.name.strip()) or creds["name"]
        return {
            "logged_in": True,
            "user": {
                "email": creds["email"],
                "username": creds["username"],
                "name": display_name,
                "avatar": "",
                "role": creds["role"],
                "auth_mode": "credentials"
            }
        }

    # 2. If password matches .env CLINICAL_PASSWORD, accept email identifier
    if env_pass and password == env_pass:
        if "@" in identifier:
            local_part = identifier.split("@")[0].replace(".", " ").replace("_", " ").title()
            display_name = (payload.name and payload.name.strip()) or (f"Dr. {local_part}" if not local_part.lower().startswith("dr") else local_part)
            return {
                "logged_in": True,
                "user": {
                    "email": identifier,
                    "username": identifier.split("@")[0],
                    "name": display_name,
                    "avatar": "",
                    "role": creds["role"],
                    "auth_mode": "credentials"
                }
            }
        else:
            display_name = (payload.name and payload.name.strip()) or f"Dr. {identifier.title()}"
            return {
                "logged_in": True,
                "user": {
                    "email": f"{identifier.lower()}@agrivision.ai",
                    "username": identifier,
                    "name": display_name,
                    "avatar": "",
                    "role": creds["role"],
                    "auth_mode": "credentials"
                }
            }

    # 3. If password did not match
    raise HTTPException(
        status_code=401,
        detail="Invalid credentials. Please verify your workstation username/email and password matching .env."
    )


@router.post("/offline-login")
def offline_evaluator_login():
    """Authenticates user in Offline Clinical Evaluator Mode."""
    return {
        "logged_in": True,
        "user": {
            "email": "agronomist.evaluator@agrivision.ai",
            "name": "Dr. Clinical Pathologist",
            "avatar": "",
            "role": "Lead Diagnostic Evaluator • ICAR Reference Suite",
            "auth_mode": "offline_evaluator"
        }
    }
