"""
Clinical Design System CSS ("Luminous Clinical White") for AgriVision Pro.
"""

import streamlit as st

CLINICAL_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

    :root {
        --bg-canvas: #F8FAFC;
        --surface-white: #FFFFFF;
        --brand-emerald: #059669;
        --brand-forest: #064E3B;
        --text-primary: #0F172A;
        --text-secondary: #334155;
        --text-muted: #64748B;
        --border-light: #E2E8F0;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
        background-color: var(--bg-canvas);
    }

    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
        max-width: 1400px;
    }

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    /* Google OAuth Card Styling */
    .oauth-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 36px 10px;
    }

    .oauth-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        box-shadow: 0 10px 25px -3px rgba(15, 23, 42, 0.06), 0 25px 50px -12px rgba(15, 23, 42, 0.08);
        width: 100%;
        padding: 32px 28px 22px 28px;
        text-align: center;
    }

    .security-badge-row {
        display: flex;
        justify-content: center;
        gap: 16px;
        margin-top: 20px;
        padding-top: 14px;
        border-top: 1px solid #E2E8F0;
        font-size: 12px;
        color: #64748B;
    }

    .security-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

    /* Clinical Header Bar */
    .clinical-header {
        background: #FFFFFF;
        color: #0F172A;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 20px 28px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03), 0 8px 24px -4px rgba(15, 23, 42, 0.04);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }

    .clinical-title {
        font-size: 1.65rem;
        font-weight: 800;
        color: #0F172A;
        margin: 0;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .clinical-subtitle {
        color: #64748B;
        font-size: 0.86rem;
        margin: 3px 0 0 0;
        font-weight: 500;
    }

    .live-model-pill {
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.80rem;
        color: #065F46;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
    }

    /* Pipeline Stepper */
    .stepper-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 12px 20px;
        margin-bottom: 22px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
        font-size: 0.84rem;
        font-weight: 600;
    }

    .step-item {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #1E293B;
    }

    .step-number {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #047857;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 700;
    }

    .step-arrow {
        color: #CBD5E1;
        font-size: 14px;
    }

    /* 3-Column Diagnostic Suite Cards */
    .diagnostic-stage-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 4px 12px -2px rgba(15, 23, 42, 0.03);
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .stage-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.70rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .stage-1-badge { background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; }
    .stage-2-badge { background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; }
    .stage-3-badge { background: #F0F9FF; color: #0284C7; border: 1px solid #BAE6FD; }

    .stage-title {
        font-size: 1.12rem;
        font-weight: 800;
        color: #0F172A;
        margin: 0 0 4px 0;
    }

    .stage-subtitle {
        font-size: 0.78rem;
        color: #64748B;
        margin-bottom: 8px;
    }

    /* Severity Badges */
    .severity-pill-mild {
        background-color: #F0FDF4;
        color: #15803D;
        border: 1px solid #BBF7D0;
        padding: 3px 10px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.80rem;
        display: inline-block;
    }
    .severity-pill-moderate {
        background-color: #FFFBEB;
        color: #B45309;
        border: 1px solid #FDE68A;
        padding: 3px 10px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.80rem;
        display: inline-block;
    }
    .severity-pill-severe {
        background-color: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FECACA;
        padding: 3px 10px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.80rem;
        display: inline-block;
    }

    .treatment-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 16px;
        height: 100%;
        color: #334155;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    }

    .treatment-title {
        font-size: 0.90rem;
        font-weight: 700;
        color: #065F46;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Metric card */
    .stat-metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 12px;
        margin-top: 8px;
        color: #1E293B;
    }

    /* Custom Streamlit Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: #ffffff;
        border-radius: 10px;
        font-weight: 600;
        border: none;
        padding: 0.55rem 1.15rem;
        box-shadow: 0 2px 6px rgba(5, 150, 105, 0.2);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: #ffffff;
        box-shadow: 0 6px 16px rgba(5, 150, 105, 0.28);
    }
</style>
"""

def apply_custom_css():
    """Applies the Luminous Clinical White CSS to Streamlit."""
    st.markdown(CLINICAL_CSS, unsafe_allow_html=True)
