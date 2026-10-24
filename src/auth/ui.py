"""
Google OAuth 2.0 User Interface and Callback Handling.
"""

import streamlit as st
from src.auth.oauth import (
    load_oauth_credentials,
    get_google_auth_url,
    exchange_code_for_user_info
)

def process_oauth_callbacks():
    """
    Checks for Google OAuth 2.0 callback codes or error parameters in the URL query string.
    Updates st.session_state accordingly.
    """
    client_id, client_secret, redirect_uri = load_oauth_credentials(default_redirect="http://localhost:8501")

    if "code" in st.query_params and not st.session_state.logged_in:
        auth_code = st.query_params.get("code")
        if client_id and client_secret:
            with st.spinner("Authenticating with Google Identity Services..."):
                success, res = exchange_code_for_user_info(auth_code, client_id, client_secret, redirect_uri)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_email = res.get("email", "")
                    st.session_state.user_name = res.get("name", "Google Agronomist")
                    st.session_state.user_avatar = res.get("picture", "")
                    st.session_state.user_role = "Authenticated Google Agronomist"
                    st.session_state.oauth_error = ""
                    st.query_params.clear()
                    st.rerun()
                else:
                    st.session_state.oauth_error = str(res)
                    st.query_params.clear()
        else:
            st.session_state.oauth_error = "Authorization code received from Google, but Client ID or Client Secret are not configured."
            st.query_params.clear()

    if "error" in st.query_params:
        st.session_state.oauth_error = f"Google Sign-In was cancelled or rejected ({st.query_params.get('error')})."
        st.query_params.clear()


def render_google_oauth_modal():
    """Renders authentic Google OAuth 2.0 Sign-In screen in Luminous Clinical White."""
    curr_client_id, curr_client_secret, curr_redirect_uri = load_oauth_credentials(default_redirect="http://localhost:8501")

    st.markdown("<div class='oauth-wrapper'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        if st.session_state.get("oauth_error"):
            st.error(f"❌ {st.session_state.oauth_error}")
            if st.button("Dismiss Message", key="btn_dismiss_err"):
                st.session_state.oauth_error = ""
                st.rerun()

        st.markdown("""
        <div class='oauth-card'>
            <svg width="44" height="44" viewBox="0 0 48 48" style="margin-bottom: 12px;">
                <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.79l7.97-6.2z"/>
                <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
            </svg>
            <h2 style='color:#0F172A; font-size:1.4rem; font-weight:800; margin:0 0 6px 0;'>Sign in to AgriVision Pro</h2>
            <p style='color:#64748B; font-size:0.88rem; margin:0 0 14px 0;'>Authenticate with Google Identity Services or enter Offline Evaluator Mode</p>
        </div>
        """, unsafe_allow_html=True)

        if curr_client_id and curr_client_secret:
            auth_url = get_google_auth_url(curr_client_id, curr_redirect_uri)
            st.markdown("<div style='margin-top: 12px;'>", unsafe_allow_html=True)
            st.link_button("🌐 Continue to Google Sign-In", auth_url, type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if st.button("⚡ Enter Clinical Workstation (Evaluator Mode)", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.user_email = "agronomist.evaluator@agrivision.ai"
            st.session_state.user_name = "Dr. Clinical Pathologist"
            st.session_state.user_role = "Lead Diagnostic Evaluator"
            st.session_state.user_avatar = "🔬"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def require_auth():
    """
    Checks if user is logged in. If not, processes callbacks or renders the login modal and stops execution.
    """
    process_oauth_callbacks()
    if not st.session_state.logged_in:
        render_google_oauth_modal()
        st.stop()
