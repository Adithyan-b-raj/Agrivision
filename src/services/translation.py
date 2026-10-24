"""
Multilingual Translation Service.
Provides offline caching and deep-translator online fallback for English, Malayalam, Hindi, and Tamil.
"""

from deep_translator import GoogleTranslator

# Language configuration
LANGUAGES = {
    "English": "en",
    "മലയാളം (Malayalam)": "ml",
    "हिन्दी (Hindi)": "hi",
    "தமிழ் (Tamil)": "ta"
}

# Static high-quality offline translation cache for common plant diagnosis strings
TRANSLATION_CACHE = {
    "ml": {
        "Live Diagnosis & Segmentation": "തത്സമയ രോഗനിർണയവും സെഗ്മെന്റേഷനും",
        "Voice Symptom Input (STT)": "വോയ്സ് രോഗലക്ഷണ ഇൻപുട്ട് (STT)",
        "Backbone Model Comparison": "ബാക്ക്ബോൺ മോഡൽ താരതമ്യം",
        "AI Generated Report (PDF)": "AI തയ്യാറാക്കിയ റിപ്പോർട്ട് (PDF)",
        "Upload Leaf Image": "ഇലയുടെ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
        "Choose a leaf image (JPG/PNG)": "ഒരു ഇല ചിത്രം തിരഞ്ഞെടുക്കുക (JPG/PNG)",
        "Input Leaf Image": "ഇൻപുട്ട് ഇല ചിത്രം",
        "Detection & Segmentation Output": "കണ്ടെത്തലും സെഗ്മെന്റേഷൻ ഔട്ട്പുട്ടും",
        "Running Detection (RT-DETR) & Segmentation (SAM2)...": "കണ്ടെത്തലും സെഗ്മെന്റേഷനും വിശകലനം ചെയ്യുന്നു...",
        "Diseased Lesions Detected & Segmented": "രോഗബാധിതമായ ഭാഗങ്ങൾ അടയാളപ്പെടുത്തി",
        "Diagnosis": "രോഗനിർണയം",
        "Confidence Score": "കൃത്യത സ്കോർ",
        "Severity Level": "തീവ്രത നില",
        "Intelligent Decision Support & Voice Readout": "തീരുമാന പിന്തുണയും ശബ്ദ അറിയിപ്പും",
        "Fertilizer Recommendation": "വളപ്രയോഗ നിർദ്ദേശം",
        "Pesticide Recommendation": "കീടനാശിനി നിർദ്ദേശം",
        "Market Impact Analysis": "വിപണി ആഘാത വിശകലനം",
        "Text-to-Speech (TTS) Voice Readout": "ശബ്ദ അറിയിപ്പ് (ടെക്സ്റ്റ്-ടു-സ്പീച്ച്)",
        "Generate & Play Voice Output": "ശബ്ദ സന്ദേശം കേൾക്കുക",
        "Generate PDF Report": "PDF റിപ്പോർട്ട് തയ്യാറാക്കുക",
        "Download Diagnosis Report (PDF)": "റിപ്പോർട്ട് ഡൗൺലോഡ് ചെയ്യുക (PDF)",
        "Multimodal Voice Input (Whisper STT)": "ശബ്ദ രോഗലക്ഷണ ഇൻപുട്ട് (Whisper STT)",
        "Farmers can describe symptoms via voice in their native language (Malayalam, Hindi, or English).": "കർഷകർക്ക് അവരുടെ സ്വന്തം ഭാഷയിൽ രോഗലക്ഷണങ്ങൾ സംസാരിച്ചു നൽകാം.",
        "Upload Audio Recording (WAV/MP3)": "ഓഡിയോ റെക്കോർഡിംഗ് അപ്‌ലോഡ് ചെയ്യുക",
        "OR choose a simulated spoken symptom test": "അല്ലെങ്കിൽ ഒരു സാമ്പിൾ ശബ്ദം തിരഞ്ഞെടുക്കുക",
        "Select Sample Spoken Symptom:": "സാമ്പിൾ രോഗലക്ഷണം തിരഞ്ഞെടുക്കുക:",
        "Transcribe & Extract Symptoms": "രോഗലക്ഷണങ്ങൾ വേർതിരിച്ചെടുക്കുക",
        "Speech Transcribed Successfully:": "ശബ്ദം വിജയകരമായി തിരിച്ചറിഞ്ഞു:",
        "Extracted Symptom Entities": "കണ്ടെത്തിയ രോഗലക്ഷണങ്ങൾ",
        "Multiple Backbone Comparison (PlantSeg Benchmark)": "വിവിധ മോഡലുകളുടെ താരതമ്യം (PlantSeg ബെഞ്ച്മാർക്ക്)",
        "Benchmarking results from Tianqi Wei et al. on the 11,400+ image in-the-wild PlantSeg dataset.": "11,400-ലധികം ചിത്രങ്ങളുള്ള PlantSeg ഡാറ്റാസെറ്റിലെ ഫലങ്ങൾ.",
        "Please run a diagnosis on Tab 1 first to generate a report.": "റിപ്പോർട്ട് തയ്യാറാക്കുന്നതിനായി ദയവായി ടാബ് 1-ൽ രോഗനിർണയം നടത്തുക."
    },
    "hi": {
        "Live Diagnosis & Segmentation": "लाइव रोग निदान एवं सेगमेंटेशन",
        "Voice Symptom Input (STT)": "ध्वनि लक्षण इनपुट (STT)",
        "Backbone Model Comparison": "बैकबोन मॉडल तुलना",
        "AI Generated Report (PDF)": "एआई जनरेटेड रिपोर्ट (PDF)",
        "Upload Leaf Image": "पत्ती की छवि अपलोड करें",
        "Choose a leaf image (JPG/PNG)": "पत्ती की तस्वीर चुनें (JPG/PNG)",
        "Input Leaf Image": "इनपुट पत्ती की छवि",
        "Detection & Segmentation Output": "डिटेक्शन एवं सेगमेंटेशन परिणाम",
        "Running Detection (RT-DETR) & Segmentation (SAM2)...": "डिटेक्शन और सेगमेंटेशन प्रक्रिया जारी है...",
        "Diseased Lesions Detected & Segmented": "रोगग्रस्त धब्बे चिन्हित एवं विभाजित",
        "Diagnosis": "रोग निदान",
        "Confidence Score": "सटीकता स्कोर",
        "Severity Level": "गंभीरता स्तर",
        "Intelligent Decision Support & Voice Readout": "निर्णय सहायता एवं ध्वनि वाचन",
        "Fertilizer Recommendation": "उर्वरक सुझाव",
        "Pesticide Recommendation": "कीटनाशक सुझाव",
        "Market Impact Analysis": "बाजार एवं उपज प्रभाव विश्लेषण",
        "Text-to-Speech (TTS) Voice Readout": "ध्वनि वाचन (टेक्स्ट-टू-स्पीच)",
        "Generate & Play Voice Output": "आवाज में संदेश सुनें",
        "Generate PDF Report": "PDF रिपोर्ट तैयार करें",
        "Download Diagnosis Report (PDF)": "रिपोर्ट डाउनलोड करें (PDF)",
        "Multimodal Voice Input (Whisper STT)": "ध्वनि लक्षण इनपुट (Whisper STT)",
        "Farmers can describe symptoms via voice in their native language (Malayalam, Hindi, or English).": "किसान अपनी भाषा में बोलकर लक्षण बता सकते हैं।",
        "Upload Audio Recording (WAV/MP3)": "ऑडियो रिकॉर्डिंग अपलोड करें",
        "OR choose a simulated spoken symptom test": "या एक नमूना ध्वनि लक्षण चुनें",
        "Select Sample Spoken Symptom:": "नमूना लक्षण चुनें:",
        "Transcribe & Extract Symptoms": "लक्षणों का विश्लेषण करें",
        "Speech Transcribed Successfully:": "ध्वनि सफलतापूर्वक पहचानी गई:",
        "Extracted Symptom Entities": "निकाले गए लक्षण",
        "Multiple Backbone Comparison (PlantSeg Benchmark)": "विभिन्न बैकबोन मॉडलों की तुलना (PlantSeg)",
        "Benchmarking results from Tianqi Wei et al. on the 11,400+ image in-the-wild PlantSeg dataset.": "11,400+ छवियों पर आधारित PlantSeg अध्ययन परिणाम।",
        "Please run a diagnosis on Tab 1 first to generate a report.": "रिपोर्ट बनाने से पहले कृपया टैब 1 में पत्ती की जांच करें।"
    },
    "ta": {
        "Live Diagnosis & Segmentation": "நேரடி நோய் கண்டறிதல் மற்றும் பிரித்தல்",
        "Voice Symptom Input (STT)": "குரல் அறிகுறி உள்ளீடு (STT)",
        "Backbone Model Comparison": "மாதிரி ஒப்பீடு",
        "AI Generated Report (PDF)": "AI கண்டறிதல் அறிக்கை (PDF)",
        "Upload Leaf Image": "இலை படத்தை பதிவேற்றவும்",
        "Choose a leaf image (JPG/PNG)": "இலை படத்தைத் தேர்ந்தெடுக்கவும் (JPG/PNG)",
        "Fertilizer Recommendation": "உர பரிந்துரை",
        "Pesticide Recommendation": "பூச்சிக்கொல்லி பரிந்துரை",
        "Market Impact Analysis": "சந்தை மற்றும் மகசூல் தாக்கம்",
        "Text-to-Speech (TTS) Voice Readout": "குரல் வாசிப்பு (TTS)",
        "Generate & Play Voice Output": "குரல் செய்தியைக் கேட்கவும்",
        "Download Diagnosis Report (PDF)": "அறிக்கையைப் பதிவிறக்கவும் (PDF)",
        "Multimodal Voice Input (Whisper STT)": "பன்மொழி குரல் உள்ளீடு (Whisper STT)",
        "Transcribe & Extract Symptoms": "அறிகுறிகளைப் பிரித்தெடுக்கவும்",
        "Speech Transcribed Successfully:": "குரல் வெற்றிகரமாக மாற்றப்பட்டது:",
        "Extracted Symptom Entities": "கண்டறியப்பட்ட அறிகுறிகள்",
        "Multiple Backbone Comparison (PlantSeg Benchmark)": "பல்வேறு மாதிரிகளின் ஒப்பீடு (PlantSeg)"
    }
}

def translate_text(text: str, target_lang_code: str) -> str:
    """Translates text into target language (en, ml, hi, ta) using offline dictionary + online fallback."""
    if not text or target_lang_code == "en":
        return text
    
    # 1. Check instant offline dictionary
    if target_lang_code in TRANSLATION_CACHE and text in TRANSLATION_CACHE[target_lang_code]:
        return TRANSLATION_CACHE[target_lang_code][text]
        
    # 2. Online Google Translator
    try:
        translated = GoogleTranslator(source='auto', target=target_lang_code).translate(text)
        return translated if translated else text
    except Exception:
        # Fallback cleanly to original text
        return text
