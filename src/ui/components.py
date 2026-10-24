"""
Reusable UI Components: Header, Stepper, and Status Badges.
"""

import streamlit as st

def render_clinical_header(num_classes: int = 115):
    """Renders the top clinical header bar with active model pill."""
    st.markdown(f"""
    <div class='clinical-header'>
        <div>
            <h1 class='clinical-title'>🌿 AgriVision Pro</h1>
            <p class='clinical-subtitle'>Clinical Plant Disease Diagnosis, Mask Segmentation & Multimodal Decision Support</p>
        </div>
        <div style='display:flex; flex-direction:column; align-items:flex-end; gap:6px;'>
            <div class='live-model-pill'>
                <span class='status-dot'></span>
                <b>Active:</b> ConvNeXt V2 ({num_classes} Classes) &nbsp;|&nbsp; <b>Precision:</b> High-Accuracy Standard
            </div>
            <div style='font-size:0.76rem; color:#64748B; font-weight:500;'>
                STIST Trivandrum • ICAR Pathology Research Reference Suite
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_pipeline_stepper():
    """Renders the 4-step horizontal pipeline progress bar."""
    st.markdown("""
    <div class='stepper-container'>
        <div class='step-item'>
            <span class='step-number'>1</span>
            <span>Image Acquisition</span>
        </div>
        <span class='step-arrow'>➔</span>
        <div class='step-item'>
            <span class='step-number'>2</span>
            <span>RT-DETR Lesion Detection</span>
        </div>
        <span class='step-arrow'>➔</span>
        <div class='step-item'>
            <span class='step-number'>3</span>
            <span>SAM-2 Pixel Masking</span>
        </div>
        <span class='step-arrow'>➔</span>
        <div class='step-item'>
            <span class='step-number'>4</span>
            <span>ConvNeXt V2 Classification & Rx</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
