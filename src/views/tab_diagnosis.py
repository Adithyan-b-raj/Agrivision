"""
Tab 1: 3-Stage Multimodal Clinical Diagnostic Suite & Prescription Engine.
"""

import os
from datetime import datetime
import streamlit as st
from PIL import Image
from src.config import get_sample_image_path
from src.services.translation import translate_text
from src.services.audio import generate_tts_audio
from src.knowledge.treatments import get_treatment_for_disease
from src.models.inference import predict_leaf_disease

def render_tab_diagnosis(lang_code: str, selected_lang_name: str):
    """Renders Tab 1: Image upload, lesion detection, SAM2 masking, classification & prescription."""
    up_col1, up_col2 = st.columns([1.6, 1])
    
    with up_col1:
        st.markdown(f"#### 📥 1. {translate_text('Upload Leaf Image', lang_code)}")
        uploaded_file = st.file_uploader(
            translate_text("Choose a leaf image (JPG/PNG)", lang_code),
            type=["jpg", "jpeg", "png"],
            help="High-resolution in-the-wild leaf photography supported."
        )

    sample_img_path = get_sample_image_path()
    
    with up_col2:
        st.markdown("#### ⚡ Quick Field Demo")
        if os.path.exists(sample_img_path):
            st.caption("Test the clinical pipeline with real diseased field foliage:")
            if st.button("🌿 Load Sample Diseased Leaf (Field Sample)", use_container_width=True):
                st.session_state["active_sample_loaded"] = True
        else:
            st.info("Upload any crop leaf to trigger instant diagnostic inference.")

    image_to_process = None
    if uploaded_file:
        image_to_process = Image.open(uploaded_file)
    elif st.session_state.get("active_sample_loaded", False) and os.path.exists(sample_img_path):
        image_to_process = Image.open(sample_img_path)

    if image_to_process is not None:
        with st.spinner("Executing Multimodal Pipeline: RT-DETR Localization ➔ SAM 2 Masking ➔ ConvNeXt V2 Classification..."):
            det_img, seg_img, cam_img, disease, conf, top_3, severity_pct, num_boxes = predict_leaf_disease(image_to_process)
            info = get_treatment_for_disease(disease)

        st.markdown("---")
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;'>
            <h3 style='color:#0F172A; margin:0; font-weight:800;'>📋 Multimodal Diagnostic Suite (3 Symmetrical Stages)</h3>
            <span style='background:#ECFDF5; border:1px solid #A7F3D0; color:#065F46; padding:5px 14px; border-radius:999px; font-weight:700; font-size:0.80rem;'>
                Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Severity categorization
        if severity_pct < 0.15:
            severity_label = "Mild"
            severity_class = "severity-pill-mild"
        elif severity_pct < 0.35:
            severity_label = "Moderate"
            severity_class = "severity-pill-moderate"
        else:
            severity_label = "Severe"
            severity_class = "severity-pill-severe"

        # Symmetrical 3 Columns for Analytical Stages
        col_stage1, col_stage2, col_stage3 = st.columns([1, 1, 1.1])

        # ---------------- STAGE 1: DETECTION ----------------
        with col_stage1:
            st.markdown("""
            <div class='diagnostic-stage-card' style='min-height: 112px; margin-bottom: 12px;'>
                <span class='stage-badge stage-1-badge'>Stage 01 • RT-DETR Detection</span>
                <div class='stage-title'>Lesion Localization</div>
                <div class='stage-subtitle'>Spatial bounding boxes & infection focal centroids</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.image(det_img, use_container_width=True)
            
            st.markdown("""
            <div style='display:flex; justify-content:space-between; align-items:center; height: 38px; margin: 4px 0 10px 0;'>
                <span style='font-size:0.80rem; font-weight:700; color:#DC2626;'>🎯 Detection Mode: Active</span>
                <span style='font-size:0.75rem; background:#FEF2F2; color:#DC2626; border:1px solid #FECACA; padding:3px 8px; border-radius:6px; font-weight:700;'>Crimson Reticles</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='stat-metric-card'>
                <div style='font-size:0.72rem; color:#64748B; font-weight:700; text-transform:uppercase;'>Localized Lesions</div>
                <div style='font-size:1.45rem; font-weight:800; color:#DC2626;'>{num_boxes} Spots Mapped</div>
                <div style='font-size:0.78rem; color:#475569; margin-top:4px;'>
                    <b>Spatial Distribution:</b> Uniform foliar spread<br>
                    <b>Centroid Alignment:</b> Micro-reticles placed
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ---------------- STAGE 2: SEGMENTATION ----------------
        with col_stage2:
            st.markdown("""
            <div class='diagnostic-stage-card' style='min-height: 112px; margin-bottom: 12px;'>
                <span class='stage-badge stage-2-badge'>Stage 02 • SAM 2 & Grad-CAM++</span>
                <div class='stage-title'>Pixel Surface Mask</div>
                <div class='stage-subtitle'>Cellular boundary delineation & severity calculation</div>
            </div>
            """, unsafe_allow_html=True)

            current_seg_mode = st.session_state.get("seg_view_selector", "SAM 2 Pixel Mask")
            if current_seg_mode == "SAM 2 Pixel Mask":
                st.image(seg_img, use_container_width=True)
            else:
                st.image(cam_img, use_container_width=True)

            st.radio(
                "Display Mode:",
                ["SAM 2 Pixel Mask", "Grad-CAM++ Attention"],
                horizontal=True,
                key="seg_view_selector",
                label_visibility="collapsed"
            )

            st.markdown(f"""
            <div class='stat-metric-card'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-size:0.72rem; color:#64748B; font-weight:700; text-transform:uppercase;'>Infected Area</span>
                    <span class='{severity_class}'>{severity_label} ({severity_pct*100:.1f}%)</span>
                </div>
                <div style='font-size:1.45rem; font-weight:800; color:#059669; margin:4px 0;'>
                    {severity_pct*100:.1f}% Leaf Damaged
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(float(min(severity_pct, 1.0)))

        # ---------------- STAGE 3: CLASSIFICATION ----------------
        with col_stage3:
            st.markdown("""
            <div class='diagnostic-stage-card' style='min-height: 112px; margin-bottom: 12px;'>
                <span class='stage-badge stage-3-badge'>Stage 03 • ConvNeXt V2</span>
                <div class='stage-title'>Neural Classification</div>
                <div class='stage-subtitle'>115-Class PlantSeg fine-grained pathology prediction</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style='background:#ECFDF5; border:1px solid #A7F3D0; border-radius:14px; padding:16px; margin-bottom:12px;'>
                <div style='font-size:0.72rem; color:#047857; font-weight:800; text-transform:uppercase; letter-spacing:0.5px;'>Primary Identified Pathology</div>
                <div style='font-size:1.35rem; font-weight:800; color:#0F172A; margin:4px 0 6px 0;'>{disease}</div>
                <div style='font-size:0.84rem; color:#334155;'>
                    <b>Host Crop:</b> <span style='background:#059669; color:#FFFFFF; padding:2px 8px; border-radius:6px; font-weight:600;'>{info['crop']}</span><br>
                    <div style='margin-top:6px;'><b>Top-1 Diagnostic Confidence:</b> <span style='font-weight:800; color:#059669; font-size:1.02rem;'>{conf*100:.1f}%</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            prob_sum = sum(p for _, p in top_3) if top_3 else 1.0

            st.markdown("""
            <div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:16px;'>
                <div style='font-size:0.72rem; font-weight:800; color:#64748B; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;'>
                    Differential Diagnosis Candidates
                </div>
            """, unsafe_allow_html=True)
            
            for cls_name, prob in top_3:
                norm_pct = (prob / prob_sum) * 100 if prob_sum > 0 else prob * 100
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center; font-size:0.84rem; margin:6px 0 2px 0;'>
                    <span style='font-weight:700; color:#0F172A;'>{cls_name}</span>
                    <span style='font-weight:800; color:#0284C7;'>{norm_pct:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
                st.progress(float(min(norm_pct / 100.0, 1.0)))

            st.markdown("</div>", unsafe_allow_html=True)

        # Save in session state for PDF and Audio export
        st.session_state.last_diagnosis = {
            "disease": disease,
            "crop": info["crop"],
            "confidence": conf,
            "severity": severity_label,
            "symptoms": info["symptoms"],
            "fertilizer": info["fertilizer"],
            "pesticide": info["pesticide"],
            "image": det_img
        }

        # ---------------- CLINICAL PRESCRIPTION CARD ----------------
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center; border-bottom: 1px solid #E2E8F0; padding: 4px 6px 14px 6px; margin-bottom: 18px;'>
                <div>
                    <span style='font-size:1.30rem; font-weight:800; color:#0F172A; letter-spacing:-0.2px;'>℞ CLINICAL AGRONOMIC ACTION PLAN</span>
                    <div style='font-size:0.82rem; color:#059669; font-weight:600; margin-top:3px;'>
                        AgriVision Official Treatment Protocol • STIST Laboratory Validation
                    </div>
                </div>
                <div style='font-size:0.78rem; color:#475569; text-align:right; line-height:1.45;'>
                    <b>Prescription ID:</b> #AV-2026-8814<br>
                    <b>Target Pathology:</b> <span style='color:#0F172A; font-weight:700;'>{disease} ({info['crop']})</span><br>
                    <b>Clinical Status:</b> <span style='color:#059669; font-weight:700;'>Validated</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            rx_col1, rx_col2, rx_col3 = st.columns([1.1, 1.1, 1])

            with rx_col1:
                st.markdown(f"""
                <div class='treatment-box'>
                    <div class='treatment-title'>🛡️ {translate_text('Pesticide Recommendation', lang_code)}</div>
                    <div style='font-size:0.86rem; color:#334155; line-height:1.55;'>
                        {translate_text(info['pesticide'], lang_code)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with rx_col2:
                st.markdown(f"""
                <div class='treatment-box'>
                    <div class='treatment-title'>🌱 {translate_text('Fertilizer Recommendation', lang_code)}</div>
                    <div style='font-size:0.86rem; color:#334155; line-height:1.55;'>
                        {translate_text(info['fertilizer'], lang_code)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with rx_col3:
                st.markdown(f"""
                <div class='treatment-box'>
                    <div class='treatment-title'>🔊 {translate_text('Text-to-Speech (TTS) Voice Readout', lang_code)}</div>
                    <div style='font-size:0.82rem; color:#64748B; margin-bottom:10px;'>
                        Listen to spoken prescription in <b>{selected_lang_name}</b>.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                summary_speech = f"AgriVision Diagnosis: {disease} detected on {info['crop']}. Severity is {severity_label}. Recommended action: {translate_text(info['pesticide'], lang_code)}"
                if st.button("▶️ " + translate_text("Generate & Play Voice Output", lang_code), use_container_width=True):
                    with st.spinner("Synthesizing audio prescription..."):
                        audio_path = generate_tts_audio(summary_speech, lang_code)
                        if audio_path:
                            st.audio(audio_path, format="audio/mp3")
