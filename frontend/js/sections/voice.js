/**
 * Section 2 Controller: Multimodal Voice Input (Whisper STT & NLP Symptom Entity Extraction)
 */

window.VoiceSection = {
    isRecording: false,
    recognition: null,

    init() {
        const runBtn = document.getElementById("btn-run-stt");
        const audioInput = document.getElementById("voice-audio-input");
        const audioDrop = document.getElementById("voice-audio-dropzone");
        const micBtn = document.getElementById("btn-live-mic");

        if (runBtn) {
            runBtn.addEventListener("click", () => this.runPresetOrCustomAnalysis());
        }

        if (audioDrop && audioInput) {
            audioDrop.addEventListener("click", () => audioInput.click());
            audioInput.addEventListener("change", (e) => {
                if (e.target.files && e.target.files[0]) {
                    this.handleAudioFileUpload(e.target.files[0]);
                }
            });
        }

        if (micBtn) {
            micBtn.addEventListener("click", () => this.toggleLiveMic());
        }
    },

    toggleLiveMic() {
        const micBtn = document.getElementById("btn-live-mic");
        const customInput = document.getElementById("stt-custom-textarea");
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            alert("Browser Speech Recognition API is not supported in this browser. Please use the sample selector, type symptoms, or upload an audio file.");
            return;
        }

        if (this.isRecording && this.recognition) {
            this.recognition.stop();
            return;
        }

        this.recognition = new SpeechRecognition();
        const langMap = { en: "en-IN", ml: "ml-IN", hi: "hi-IN", ta: "ta-IN" };
        this.recognition.lang = langMap[window.AppState.lang] || "en-US";
        this.recognition.interimResults = false;

        this.recognition.onstart = () => {
            this.isRecording = true;
            if (micBtn) {
                micBtn.classList.add("bg-red-600", "text-white", "pulse-mic");
                micBtn.innerHTML = `🔴 <span>Listening... (Click to Stop)</span>`;
            }
        };

        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            if (customInput) {
                customInput.value = transcript;
            }
            this.runPresetOrCustomAnalysis(transcript);
        };

        this.recognition.onend = () => {
            this.isRecording = false;
            if (micBtn) {
                micBtn.classList.remove("bg-red-600", "text-white", "pulse-mic");
                micBtn.innerHTML = `🎙️ <span>Speak Live into Microphone</span>`;
            }
        };

        this.recognition.start();
    },

    async handleAudioFileUpload(file) {
        const out = document.getElementById("stt-output-panel");
        if (!out) return;
        out.innerHTML = this.getLoadingHtml(`Transcribing audio file "${file.name}" with Whisper STT...`);
        try {
            const res = await window.AgriAPI.uploadVoiceAudio(file, window.AppState.lang);
            this.renderEntityResults(res);
        } catch (err) {
            out.innerHTML = `<div class="p-4 rounded-xl bg-red-50 border border-red-200 text-xs text-red-700">⚠️ ${err.message}</div>`;
        }
    },

    async runPresetOrCustomAnalysis(overrideText = null) {
        const out = document.getElementById("stt-output-panel");
        const picker = document.getElementById("stt-sample-select");
        const customBox = document.getElementById("stt-custom-textarea");
        if (!out) return;

        const customText = overrideText !== null ? overrideText : (customBox ? customBox.value.trim() : "");
        const sampleId = picker ? picker.value : "citrus_en";

        out.innerHTML = this.getLoadingHtml("Running Whisper Speech-to-Text & Agricultural Entity Resolution...");

        try {
            const res = await window.AgriAPI.analyzeVoice(sampleId, customText || null, window.AppState.lang);
            this.renderEntityResults(res);
        } catch (err) {
            out.innerHTML = `<div class="p-4 rounded-xl bg-red-50 border border-red-200 text-xs text-red-700">⚠️ ${err.message}</div>`;
        }
    },

    getLoadingHtml(msg) {
        return `
            <div class="studio-card p-8 text-center">
                <div class="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center mx-auto mb-3">
                    <div class="w-5 h-5 border-2 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
                </div>
                <div class="text-sm font-bold text-slate-900">${msg}</div>
                <div class="text-xs text-slate-500 mt-1">Parsing host crop, lesion morphology, and pathogen signatures</div>
            </div>
        `;
    },

    renderEntityResults(data) {
        const out = document.getElementById("stt-output-panel");
        if (!out) return;

        out.innerHTML = `
            <div class="space-y-4 section-fade">
                <!-- Transcribed Speech Bubble -->
                <div class="studio-card p-5 border-l-4 border-l-emerald-600 bg-gradient-to-r from-emerald-50/50 to-white">
                    <div class="flex items-center justify-between mb-1.5">
                        <span class="text-xs font-bold uppercase tracking-wider text-emerald-700 flex items-center gap-1.5">
                            🗣️ ${window.t("Speech Transcribed Successfully:")}
                        </span>
                        <span class="px-2.5 py-0.5 rounded-full text-[11px] font-mono-tech font-bold bg-emerald-100 text-emerald-800">
                            Whisper-v3 Large • ${data.confidence}% Match
                        </span>
                    </div>
                    <p class="text-base font-semibold italic text-slate-900 leading-relaxed">
                        "${data.transcript}"
                    </p>
                    ${data.english_translation ? `
                        <p class="text-xs text-slate-500 mt-1.5 pt-1.5 border-t border-slate-200/70">
                            <b>English Translation:</b> "${data.english_translation}"
                        </p>
                    ` : ""}
                </div>

                <!-- 4-Card Extracted Entities Grid -->
                <div>
                    <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2.5">
                        📋 ${window.t("extracted_entities")}
                    </h4>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                        <div class="studio-card p-4">
                            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Host Specimen</div>
                            <div class="text-sm font-bold text-slate-900 mt-1 flex items-center gap-2">
                                <span class="text-base">🌿</span> ${data.host_specimen}
                            </div>
                        </div>
                        <div class="studio-card p-4">
                            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Lesion Morphology</div>
                            <div class="text-sm font-bold text-slate-900 mt-1 flex items-center gap-2">
                                <span class="text-base">🔍</span> ${data.lesion_morphology}
                            </div>
                        </div>
                        <div class="studio-card p-4">
                            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Foliage Reaction</div>
                            <div class="text-sm font-bold text-slate-900 mt-1 flex items-center gap-2">
                                <span class="text-base">🍂</span> ${data.foliage_reaction}
                            </div>
                        </div>
                        <div class="studio-card p-4 bg-red-50/40 border-red-200">
                            <div class="text-[11px] font-bold uppercase tracking-wider text-red-600">Diagnosed Entity</div>
                            <div class="text-sm font-extrabold text-red-700 mt-1 flex items-center gap-2">
                                <span class="text-base">🦠</span> ${data.diagnosed_entity}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Recommended Action Protocol from Voice Diagnosis -->
                ${data.treatment ? `
                    <div class="studio-card p-5 bg-slate-50/70">
                        <div class="text-xs font-bold uppercase tracking-wider text-emerald-800 mb-3 flex items-center gap-2">
                            <span>℞</span> Recommended Field Protocol for ${data.diagnosed_entity}
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                            <div class="p-3.5 rounded-xl bg-white border border-slate-200/80">
                                <div class="font-bold text-slate-800 mb-1">🛡️ Curative Spray</div>
                                <div class="text-slate-600 leading-relaxed">${data.treatment.pesticide}</div>
                            </div>
                            <div class="p-3.5 rounded-xl bg-white border border-slate-200/80">
                                <div class="font-bold text-slate-800 mb-1">🌱 Nutrient Recovery</div>
                                <div class="text-slate-600 leading-relaxed">${data.treatment.fertilizer}</div>
                            </div>
                        </div>
                    </div>
                ` : ""}
            </div>
        `;
    }
};
