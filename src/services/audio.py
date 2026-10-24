"""
Audio and Speech Services.
Handles Text-to-Speech (TTS) audio generation.
"""

import tempfile
from gtts import gTTS

def generate_tts_audio(text: str, lang_code: str) -> str:
    """Converts diagnosis text to speech in target language and returns temp audio path."""
    try:
        # gTTS supports en, hi, ml
        tts = gTTS(text=text, lang=lang_code, slow=False)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as e:
        print(f"TTS error: {e}")
        return None
