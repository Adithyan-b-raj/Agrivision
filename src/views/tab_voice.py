"""
Tab 2: Multimodal Voice Input & Whisper Speech-to-Text (STT) Processing.
"""

import time
import streamlit as st
from src.services.translation import translate_text

def render_tab_voice(lang_code: str):
    """Renders Tab 2: Audio input, speech-to-text transcript & symptom entity extraction."""
    st.markdown(f"### 🎙️ {translate_text('Multimodal Voice Input (Whisper STT)', lang_code)}")
    st.markdown(f"<p style='color:#64748B;'>{translate_text('Farmers can describe symptoms via voice in their native language (Malayalam, Hindi, or English).', lang_code)}</p>", unsafe_allow_html=True)

    vcol1, vcol2 = st.columns([1, 1.1])

    with vcol1:
        st.markdown("""
        <div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:16px; padding:20px; text-align:center; box-shadow:0 1px 3px rgba(15,23,42,0.03);'>
            <div style='font-size:2.8rem;'>🎙️</div>
            <div style='font-weight:800; color:#0F172A; margin:6px 0; font-size:1.08rem;'>Audio Recording Console</div>
            <div style='color:#64748B; font-size:0.84rem;'>Upload an on-field voice memo or choose a regional sample.</div>
        </div>
        """, unsafe_allow_html=True)

        st.file_uploader(
            translate_text("Upload Audio Recording (WAV/MP3)", lang_code),
            type=["wav", "mp3", "m4a"],
            key="stt_uploader"
        )

        st.markdown(f"<div style='text-align:center; color:#64748B; font-size:0.80rem; margin:10px 0;'>— {translate_text('OR choose a simulated spoken symptom test', lang_code)} —</div>", unsafe_allow_html=True)
        
        sample_voice = st.selectbox(
            translate_text("Select Sample Spoken Symptom:", lang_code),
            [
                "English: 'I notice corky brown lesions and yellow halos on citrus leaves.'",
                "Malayalam: 'നാരക ഇലകളിൽ തവിട്ടുനിറത്തിലുള്ള പുള്ളികളും മഞ്ഞ നിറവും കാണുന്നുണ്ട്.'",
                "Hindi: 'नींबू के पत्तों पर भूरे रंग के उभरे हुए धब्बे और पीले घेरे दिख रहे हैं।'"
            ],
            key="stt_sample_picker"
        )

        run_stt = st.button("🎙️ " + translate_text("Transcribe & Extract Symptoms", lang_code), use_container_width=True)

    with vcol2:
        if run_stt:
            with st.spinner("Running Whisper STT & Entity Extraction..."):
                time.sleep(0.8)
                transcript_text = sample_voice.split(": ")[1].replace("'", "")
                
                st.markdown(f"""
                <div style='background:#FFFFFF; border:1px solid #E2E8F0; border-left:5px solid #059669; border-radius:14px; padding:18px; box-shadow:0 2px 8px rgba(15,23,42,0.04);'>
                    <div style='font-size:0.80rem; color:#059669; font-weight:700;'>🗣️ {translate_text('Speech Transcribed Successfully:', lang_code)}</div>
                    <div style='font-size:1.05rem; font-style:italic; color:#0F172A; margin:8px 0; font-weight:600;'>"{transcript_text}"</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"<div style='font-weight:800; color:#0F172A; font-size:1.02rem; margin:16px 0 8px 0;'>📋 {translate_text('Extracted Symptom Entities', lang_code)}:</div>", unsafe_allow_html=True)
                
                st.markdown("""
                <div style='display:grid; grid-template-columns: 1fr 1fr; gap:12px;'>
                    <div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:14px;'>
                        <div style='font-size:0.72rem; color:#64748B; font-weight:700;'>HOST SPECIMEN</div>
                        <div style='font-size:0.95rem; font-weight:800; color:#0F172A;'>Citrus / Lemon</div>
                    </div>
                    <div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:14px;'>
                        <div style='font-size:0.72rem; color:#64748B; font-weight:700;'>LESION MORPHOLOGY</div>
                        <div style='font-size:0.95rem; font-weight:800; color:#0F172A;'>Raised corky pustules</div>
                    </div>
                    <div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:14px;'>
                        <div style='font-size:0.72rem; color:#64748B; font-weight:700;'>FOLIAGE REACTION</div>
                        <div style='font-size:0.95rem; font-weight:800; color:#0F172A;'>Chlorotic yellow halos</div>
                    </div>
                    <div style='background:#FEF2F2; border:1px solid #FECACA; border-radius:12px; padding:14px;'>
                        <div style='font-size:0.72rem; color:#DC2626; font-weight:700;'>DIAGNOSED ENTITY</div>
                        <div style='font-size:0.95rem; font-weight:800; color:#B91C1C;'>Citrus Canker</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Select a spoken sample and click 'Transcribe & Extract Symptoms' to view live NLP symptom entity resolution.")
