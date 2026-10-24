/**
 * AgriVision Pro — Async REST API Client
 */

window.AgriAPI = {
    async getAuthConfig() {
        const res = await fetch("/api/auth/config", { cache: "no-store" });
        if (!res.ok) throw new Error("Failed to load auth config");
        return res.json();
    },

    async exchangeGoogleCode(code, redirectUri) {
        const res = await fetch("/api/auth/google-exchange", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code, redirect_uri: redirectUri })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Google authentication failed");
        return data;
    },

    async offlineLogin() {
        const res = await fetch("/api/auth/offline-login", { method: "POST" });
        if (!res.ok) throw new Error("Offline login failed");
        return res.json();
    },

    async credentialsLogin(identifier, password, name = null) {
        const res = await fetch("/api/auth/credentials-login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username_or_email: identifier,
                email: identifier,
                username: identifier,
                password,
                name
            })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Invalid credentials");
        return data;
    },

    async getTelemetry() {
        const res = await fetch("/api/benchmark/telemetry");
        if (!res.ok) throw new Error("Failed to load system telemetry");
        return res.json();
    },

    async analyzeLeafFile(file, lang = "en") {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("lang", lang);

        const res = await fetch("/api/diagnose/analyze", {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Diagnosis failed");
        return data;
    },

    async analyzeSampleLeaf(lang = "en") {
        const res = await fetch(`/api/diagnose/sample?lang=${encodeURIComponent(lang)}`, {
            method: "POST"
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Sample diagnosis failed");
        return data;
    },

    async translatePrescription(rawRx, lang) {
        const res = await fetch("/api/diagnose/translate-rx", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                pesticide: rawRx.pesticide,
                fertilizer: rawRx.fertilizer,
                symptoms: rawRx.symptoms,
                market_impact: rawRx.market_impact || "",
                lang
            })
        });
        if (!res.ok) throw new Error("Translation failed");
        return res.json();
    },

    async analyzeVoice(sampleId, customText, lang = "en") {
        const res = await fetch("/api/voice/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                sample_id: sampleId,
                custom_text: customText,
                lang
            })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Voice analysis failed");
        return data;
    },

    async uploadVoiceAudio(file, lang = "en") {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("lang", lang);
        const res = await fetch("/api/voice/upload-audio", {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Audio upload analysis failed");
        return data;
    },

    async synthesizeTTS(text, lang = "en") {
        const res = await fetch("/api/voice/tts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, lang })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "TTS synthesis failed");
        return data;
    },

    async downloadReportPDF(diagnosis) {
        const payload = diagnosis ? {
            disease: diagnosis.disease,
            crop: diagnosis.crop,
            confidence: diagnosis.confidence_raw || (diagnosis.confidence / 100),
            severity: diagnosis.severity.label,
            symptoms: diagnosis.treatment.raw.symptoms,
            fertilizer: diagnosis.treatment.raw.fertilizer,
            pesticide: diagnosis.treatment.raw.pesticide,
            image_data_url: diagnosis.images.detection
        } : {};

        const res = await fetch("/api/report/pdf", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || "PDF generation failed");
        }
        return res.blob();
    }
};
