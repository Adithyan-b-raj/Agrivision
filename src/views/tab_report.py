"""
Tab 4: AI Generated PDF Clinical Diagnostic Report.
"""

import os
import tempfile
import streamlit as st
from PIL import Image
from src.services.translation import translate_text
from src.services.report import create_diagnosis_pdf

def render_tab_report(lang_code: str):
    """Renders Tab 4: Diagnosis summary sheet preview and PDF download trigger."""
    st.markdown(f"### 📄 {translate_text('AI Generated Report (PDF)', lang_code)}")
    st.markdown(f"<p style='color:#64748B;'>{translate_text('Export a formal diagnostic report containing the leaf image, detected disease, severity score, and treatment plan.', lang_code)}</p>", unsafe_allow_html=True)

    if "last_diagnosis" in st.session_state:
        diag = st.session_state.last_diagnosis
        
        rcol1, rcol2 = st.columns([1, 1.2])

        with rcol1:
            st.markdown(f"""
            <div style='background:#ffffff; border:1px solid #E2EFE7; border-radius:12px; padding:18px; box-shadow:0 4px 16px rgba(15,58,42,0.06);'>
                <div style='font-size:0.82rem; color:#1B7A4E; font-weight:700;'>PREPARED CLINICAL RECORD</div>
                <div style='font-size:1.25rem; font-weight:800; color:#0F3A2A; margin:6px 0;'>{diag['disease']}</div>
                <div style='font-size:0.86rem; color:#475569;'>
                    <b>Crop:</b> {diag['crop']}<br>
                    <b>Pathological Severity:</b> {diag['severity']}<br>
                    <b>Top-1 Confidence:</b> {diag['confidence']*100:.1f}%<br>
                    <b>Physician/Specialist:</b> {st.session_state.get('user_name', 'Clinical Pathologist')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with rcol2:
            st.markdown("#### 📥 Instant Report Generation")
            temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            Image.fromarray(diag["image"]).save(temp_img.name)
            
            pdf_path = os.path.join(tempfile.gettempdir(), "AgriVision_Diagnosis_Report.pdf")
            create_diagnosis_pdf(
                image_path=temp_img.name,
                crop_name=diag["crop"],
                disease_name=diag["disease"],
                confidence=diag["confidence"],
                severity=diag["severity"],
                symptoms=diag["symptoms"],
                fertilizer=diag["fertilizer"],
                pesticide=diag["pesticide"],
                output_pdf_path=pdf_path
            )

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ " + translate_text("Download Diagnosis Report (PDF)", lang_code),
                    data=f,
                    file_name="AgriVision_Diagnosis_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            st.success("✅ Clinical Diagnostic Report compiled and ready for download.")
    else:
        st.info("ℹ️ " + translate_text("Please run a diagnosis on Tab 1 first to generate a report.", lang_code))
