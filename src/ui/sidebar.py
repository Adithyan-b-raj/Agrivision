"""
Sidebar Navigation and Control Console.
Displays user authentication details, regional language selector, and neural specs.
"""

import streamlit as st
from src.services.translation import LANGUAGES

def render_sidebar():
    """
    Renders sidebar controls, profile metadata, and regional language selector.
    Returns: (selected_lang_name, lang_code)
    """
    with st.sidebar:
        user_avatar = st.session_state.get("user_avatar", "")
        if user_avatar and (user_avatar.startswith("http://") or user_avatar.startswith("https://")):
            avatar_html = f"<img src='{user_avatar}' style='width:60px; height:60px; border-radius:50%; border:2px solid #10B981; object-fit:cover; margin-bottom:8px;' />"
        else:
            avatar_html = f"<div style='font-size:2.2rem; margin-bottom:6px;'>{user_avatar or '🌿'}</div>"

        st.markdown(f"""
        <div style='background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 16px 12px; text-align: center; margin-bottom: 14px;'>
            {avatar_html}
            <div style='font-weight:800; color:#0F172A; font-size:1.02rem; margin-top:2px;'>{st.session_state.get('user_name', 'Pathologist')}</div>
            <div style='color:#64748B; font-size:0.76rem; font-weight:500;'>{st.session_state.get('user_role', 'Agronomist')}</div>
            <div style='color:#059669; font-size:0.75rem; font-weight:600; margin-top:3px;'>{st.session_state.get('user_email', '')}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.user_name = ""
            st.session_state.user_avatar = ""
            st.session_state.user_role = ""
            st.rerun()

        st.divider()
        
        st.markdown("### 🌐 Regional Language")
        selected_lang_name = st.selectbox(
            "Interface Language:",
            list(LANGUAGES.keys()),
            index=0,
            help="Select language for diagnostic output, voice synthesizer, and UI terms."
        )
        lang_code = LANGUAGES[selected_lang_name]

        st.divider()

        st.markdown("### 🧬 Primary Neural Backbone")
        st.markdown("""
        <div style='background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 14px; font-size: 0.82rem;'>
            <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
                <span style='color:#64748B; font-weight:600;'>Model:</span>
                <span style='color:#0F172A; font-weight:700;'>ConvNeXt V2 (Tiny)</span>
            </div>
            <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
                <span style='color:#64748B; font-weight:600;'>Dataset:</span>
                <span style='color:#0F172A; font-weight:700;'>PlantSeg (115 Classes)</span>
            </div>
            <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
                <span style='color:#64748B; font-weight:600;'>Top-1 Accuracy:</span>
                <span style='color:#059669; font-weight:800; font-size:0.90rem;'>80.80%</span>
            </div>
            <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
                <span style='color:#64748B; font-weight:600;'>Top-5 Accuracy:</span>
                <span style='color:#059669; font-weight:800; font-size:0.90rem;'>97.21%</span>
            </div>
            <div style='display:flex; justify-content:space-between;'>
                <span style='color:#64748B; font-weight:600;'>Inference Speed:</span>
                <span style='color:#0284C7; font-weight:700;'>14.2 ms (FP16)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.caption("AgriVision Pro v3.0 • Developed at STIST CSE Dept.")

        return selected_lang_name, lang_code
