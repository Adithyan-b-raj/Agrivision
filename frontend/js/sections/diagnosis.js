/**
 * Section 1 Controller: Live Diagnosis, 3-Stage Multimodal Suite & Clinical Action Plan
 */

window.DiagnosisSection = {
    activeStage2Mode: "segmentation", // "segmentation" | "gradcam" | "original"

    init() {
        const dropzone = document.getElementById("leaf-dropzone");
        const fileInput = document.getElementById("leaf-file-input");
        const sampleBtn = document.getElementById("btn-load-sample");

        if (dropzone && fileInput) {
            dropzone.addEventListener("click", () => fileInput.click());
            dropzone.addEventListener("dragover", (e) => {
                e.preventDefault();
                dropzone.classList.add("dragover");
            });
            dropzone.addEventListener("dragleave", () => {
                dropzone.classList.remove("dragover");
            });
            dropzone.addEventListener("drop", (e) => {
                e.preventDefault();
                dropzone.classList.remove("dragover");
                if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                    this.handleFileUpload(e.dataTransfer.files[0]);
                }
            });
            fileInput.addEventListener("change", (e) => {
                if (e.target.files && e.target.files[0]) {
                    this.handleFileUpload(e.target.files[0]);
                }
            });
        }

        if (sampleBtn) {
            sampleBtn.addEventListener("click", () => this.handleSampleRun());
        }
    },

    setPipelineStep(activeStepIndex) {
        for (let i = 1; i <= 4; i++) {
            const el = document.getElementById(`pipeline-step-${i}`);
            if (!el) continue;
            el.classList.remove("step-active", "step-done");
            if (i < activeStepIndex) {
                el.classList.add("step-done");
            } else if (i === activeStepIndex) {
                el.classList.add("step-active");
            }
        }
    },

    completeAllSteps() {
        for (let i = 1; i <= 4; i++) {
            const el = document.getElementById(`pipeline-step-${i}`);
            if (el) {
                el.classList.remove("step-active");
                el.classList.add("step-done");
            }
        }
    },

    showScanningState(previewUrl = null, label = "Executing Multimodal Pipeline: RT-DETR ➔ SAM 2 ➔ ConvNeXt V2...") {
        const container = document.getElementById("diagnosis-results-area");
        if (!container) return;

        this.setPipelineStep(1);
        setTimeout(() => this.setPipelineStep(2), 350);
        setTimeout(() => this.setPipelineStep(3), 750);
        setTimeout(() => this.setPipelineStep(4), 1150);

        container.innerHTML = `
            <div class="studio-card p-8 text-center my-6 section-fade">
                <div class="max-w-md mx-auto">
                    ${previewUrl ? `
                        <div class="diagnostic-viewport mb-5 max-w-xs mx-auto shadow-md">
                            <div class="laser-scanner"></div>
                            <img src="${previewUrl}" alt="Scanning Leaf" />
                        </div>
                    ` : `
                        <div class="w-14 h-14 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center mx-auto mb-4">
                            <div class="w-6 h-6 border-2 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
                        </div>
                    `}
                    <h4 class="text-base font-bold text-slate-900 mb-1">${label}</h4>
                    <p class="text-xs text-slate-500">Isolating focal lesions, computing cellular SAM-2 masks & running 115-class inference</p>
                </div>
            </div>
        `;
    },

    async handleFileUpload(file) {
        const reader = new FileReader();
        reader.onload = async (e) => {
            this.showScanningState(e.target.result, `Analyzing "${file.name}"...`);
            try {
                const res = await window.AgriAPI.analyzeLeafFile(file, window.AppState.lang);
                window.AppState.lastDiagnosis = res;
                this.completeAllSteps();
                this.renderResults(res);
                window.ReportSection.renderReportView();
            } catch (err) {
                this.renderError(err.message);
            }
        };
        reader.readAsDataURL(file);
    },

    async handleSampleRun() {
        this.showScanningState(null, "Loading Field Specimen & Running 3-Stage Neural Suite...");
        try {
            const res = await window.AgriAPI.analyzeSampleLeaf(window.AppState.lang);
            window.AppState.lastDiagnosis = res;
            this.completeAllSteps();
            this.renderResults(res);
            window.ReportSection.renderReportView();
        } catch (err) {
            this.renderError(err.message);
        }
    },

    renderError(msg) {
        const container = document.getElementById("diagnosis-results-area");
        if (!container) return;
        container.innerHTML = `
            <div class="studio-card p-5 border-red-200 bg-red-50/60 text-red-800 my-4 flex items-center justify-between">
                <div class="flex items-center gap-3">
                    <span class="text-lg">⚠️</span>
                    <div>
                        <div class="font-bold text-sm">Diagnostic Pipeline Notice</div>
                        <div class="text-xs text-red-600">${msg}</div>
                    </div>
                </div>
            </div>
        `;
    },

    switchStage2View(mode) {
        this.activeStage2Mode = mode;
        const diag = window.AppState.lastDiagnosis;
        if (!diag) return;

        const imgEl = document.getElementById("stage2-viewport-img");
        const captionEl = document.getElementById("stage2-mode-caption");
        if (imgEl) {
            if (mode === "segmentation") {
                imgEl.src = diag.images.segmentation;
                if (captionEl) captionEl.textContent = "SAM 2.1 Instance Mask (Cyan/Gold Contours)";
            } else if (mode === "gradcam") {
                imgEl.src = diag.images.gradcam;
                if (captionEl) captionEl.textContent = "Grad-CAM++ Layer Activation Heatmap";
            } else {
                imgEl.src = diag.images.original;
                if (captionEl) captionEl.textContent = "Original Unprocessed Leaf Specimen";
            }
        }

        document.querySelectorAll(".stage2-seg-btn").forEach((btn) => {
            btn.classList.toggle("active", btn.dataset.mode === mode);
        });
    },

    async playPrescriptionAudio() {
        const diag = window.AppState.lastDiagnosis;
        if (!diag) return;
        const btn = document.getElementById("btn-tts-play");
        const audioHolder = document.getElementById("tts-audio-holder");
        if (!btn || !audioHolder) return;

        const origHtml = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = `<span class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span> <span>Synthesizing Voice...</span>`;

        try {
            const speechText = `AgriVision Diagnosis: ${diag.disease} detected on ${diag.crop}. Severity is ${diag.severity.label}. Recommended treatment: ${diag.treatment.pesticide}`;
            const res = await window.AgriAPI.synthesizeTTS(speechText, window.AppState.lang);
            audioHolder.innerHTML = `
                <audio controls autoplay class="w-full h-10 mt-2 rounded-lg">
                    <source src="${res.audio_data_url}" type="audio/mp3">
                </audio>
            `;
        } catch (err) {
            audioHolder.innerHTML = `<div class="text-xs text-red-600 mt-2">⚠️ ${err.message}</div>`;
        } finally {
            btn.disabled = false;
            btn.innerHTML = origHtml;
        }
    },

    renderResults(diag) {
        const container = document.getElementById("diagnosis-results-area");
        if (!container || !diag) return;

        const sevBadgeClass =
            diag.severity.key === "mild"
                ? "badge-mild"
                : diag.severity.key === "moderate"
                ? "badge-moderate"
                : "badge-severe";

        const sevBarColor =
            diag.severity.key === "mild"
                ? "bg-emerald-500"
                : diag.severity.key === "moderate"
                ? "bg-amber-500"
                : "bg-red-500";

        const diffRowsHtml = diag.differential
            .map(
                (item, idx) => `
            <div class="py-2 ${idx > 0 ? "border-t border-slate-100" : ""}">
                <div class="flex items-center justify-between gap-2 text-xs mb-1.5 min-w-0">
                    <span class="font-bold text-slate-800 flex items-center gap-1.5 min-w-0">
                        <span class="w-4 h-4 shrink-0 rounded-full ${idx === 0 ? "bg-emerald-600 text-white" : "bg-slate-100 text-slate-600"} text-[10px] flex items-center justify-center font-bold">${idx + 1}</span>
                        <span class="truncate" title="${item.disease}">${item.disease}</span>
                    </span>
                    <span class="font-mono-tech font-bold shrink-0 ${idx === 0 ? "text-emerald-700" : "text-sky-600"}">${item.relative_pct.toFixed(1)}%</span>
                </div>
                <div class="progress-track">
                    <div class="progress-fill ${idx === 0 ? "bg-emerald-500" : "bg-sky-500"}" style="width: ${Math.min(item.relative_pct, 100)}%"></div>
                </div>
            </div>
        `
            )
            .join("");

        const stage2ImgSrc =
            this.activeStage2Mode === "gradcam"
                ? diag.images.gradcam
                : this.activeStage2Mode === "original"
                ? diag.images.original
                : diag.images.segmentation;

        container.innerHTML = `
            <div class="section-fade mt-6 space-y-6">
                <!-- Suite Header Bar -->
                <div class="flex flex-wrap items-center justify-between gap-3 bg-white px-5 py-3.5 rounded-2xl border border-slate-200/90 shadow-xs">
                    <div class="flex items-center gap-3">
                        <div class="w-9 h-9 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-700 font-bold">
                            🔬
                        </div>
                        <div>
                            <h3 class="text-sm font-bold text-slate-900">Multimodal Diagnostic Suite • 3 Symmetrical Analytical Stages</h3>
                            <p class="text-xs text-slate-500">Specimen: <span class="font-medium text-slate-700">${diag.source_name}</span></p>
                        </div>
                    </div>
                    <div class="flex items-center gap-2.5 text-xs">
                        <span class="px-3 py-1 rounded-full bg-slate-100 text-slate-700 font-mono-tech font-medium border border-slate-200">
                            ⚡ ${diag.inference_ms} ms
                        </span>
                        <span class="px-3 py-1 rounded-full bg-emerald-50 text-emerald-800 font-mono-tech font-semibold border border-emerald-200">
                            🕒 ${diag.timestamp}
                        </span>
                    </div>
                </div>

                <!-- 3 Symmetrical Diagnostic Stage Columns -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-stretch">
                    
                    <!-- STAGE 01: RT-DETR DETECTION -->
                    <div class="studio-card studio-card-hover p-5 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-bold uppercase tracking-wider bg-red-50 text-red-700 border border-red-200">
                                    <span class="w-1.5 h-1.5 rounded-full bg-red-600"></span>
                                    Stage 01 • RT-DETR
                                </span>
                                <span class="text-[11px] font-mono-tech text-slate-400">Object Localization</span>
                            </div>
                            <h4 class="text-base font-bold text-slate-900">${window.t("stage1_title")}</h4>
                            <p class="text-xs text-slate-500 mb-3.5">${window.t("stage1_sub")}</p>

                            <div class="diagnostic-viewport mb-3">
                                <img src="${diag.images.detection}" alt="RT-DETR Lesion Detection" />
                            </div>

                            <div class="flex items-center justify-between px-3 py-2 rounded-lg bg-red-50/70 border border-red-100 mb-3">
                                <span class="text-xs font-semibold text-red-700 flex items-center gap-1.5">
                                    🎯 Detection Mode: Active
                                </span>
                                <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-white text-red-700 border border-red-200">
                                    Crimson Reticles
                                </span>
                            </div>
                        </div>

                        <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80">
                            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Localized Infection Foci</div>
                            <div class="flex items-baseline justify-between mt-1">
                                <div class="text-2xl font-extrabold text-red-600 font-mono-tech">${diag.num_lesions} Spots Mapped</div>
                                <span class="text-xs font-medium text-slate-500">IoU > 0.45</span>
                            </div>
                            <div class="text-xs text-slate-600 mt-2 pt-2 border-t border-slate-200/70 flex justify-between">
                                <span><b>Distribution:</b> Foliar lamina</span>
                                <span><b>Centroids:</b> Crosshair locked</span>
                            </div>
                        </div>
                    </div>

                    <!-- STAGE 02: SAM 2 & GRAD-CAM++ -->
                    <div class="studio-card studio-card-hover p-5 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-bold uppercase tracking-wider bg-emerald-50 text-emerald-700 border border-emerald-200">
                                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                                    Stage 02 • SAM 2 & XAI
                                </span>
                                <span id="stage2-mode-caption" class="text-[11px] font-mono-tech text-slate-400">SAM 2.1 Instance Mask</span>
                            </div>
                            <h4 class="text-base font-bold text-slate-900">${window.t("stage2_title")}</h4>
                            <p class="text-xs text-slate-500 mb-3.5">${window.t("stage2_sub")}</p>

                            <div class="diagnostic-viewport mb-3">
                                <img id="stage2-viewport-img" src="${stage2ImgSrc}" alt="SAM 2 Segmentation & Grad-CAM" />
                            </div>

                            <!-- Instant Zero-Reload Switcher -->
                            <div class="seg-control mb-3">
                                <button type="button" data-mode="segmentation" onclick="window.DiagnosisSection.switchStage2View('segmentation')" class="seg-btn stage2-seg-btn ${this.activeStage2Mode === "segmentation" ? "active" : ""}">
                                    ✨ SAM 2 Mask
                                </button>
                                <button type="button" data-mode="gradcam" onclick="window.DiagnosisSection.switchStage2View('gradcam')" class="seg-btn stage2-seg-btn ${this.activeStage2Mode === "gradcam" ? "active" : ""}">
                                    🔥 Grad-CAM++
                                </button>
                                <button type="button" data-mode="original" onclick="window.DiagnosisSection.switchStage2View('original')" class="seg-btn stage2-seg-btn ${this.activeStage2Mode === "original" ? "active" : ""}">
                                    🌿 Original
                                </button>
                            </div>
                        </div>

                        <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80">
                            <div class="flex items-center justify-between mb-1">
                                <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Necrotic Surface Area</span>
                                <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${sevBadgeClass}">
                                    ${diag.severity.label} (${diag.infected_area_pct}%)
                                </span>
                            </div>
                            <div class="text-2xl font-extrabold text-emerald-700 font-mono-tech mb-2">
                                ${diag.infected_area_pct}% Leaf Damaged
                            </div>
                            <div class="progress-track">
                                <div class="progress-fill ${sevBarColor}" style="width: ${Math.min(diag.infected_area_pct, 100)}%"></div>
                            </div>
                        </div>
                    </div>

                    <!-- STAGE 03: CONVNEXT V2 CLASSIFICATION -->
                    <div class="studio-card studio-card-hover p-5 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-bold uppercase tracking-wider bg-sky-50 text-sky-700 border border-sky-200">
                                    <span class="w-1.5 h-1.5 rounded-full bg-sky-600"></span>
                                    Stage 03 • ConvNeXt V2
                                </span>
                                <span class="text-[11px] font-mono-tech text-slate-400">115-Class Backbone</span>
                            </div>
                            <h4 class="text-base font-bold text-slate-900">${window.t("stage3_title")}</h4>
                            <p class="text-xs text-slate-500 mb-3.5">${window.t("stage3_sub")}</p>

                            <!-- Primary Identified Pathology Box -->
                            <div class="p-4 rounded-xl bg-gradient-to-br from-emerald-50/90 via-white to-emerald-50/40 border border-emerald-200 mb-3.5 shadow-2xs">
                                <div class="text-[11px] font-bold uppercase tracking-wider text-emerald-700">Primary Identified Pathology</div>
                                <div class="text-xl font-extrabold text-slate-900 mt-0.5 mb-2">${diag.disease}</div>
                                <div class="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-emerald-200/60 text-xs">
                                    <div>
                                        <span class="text-slate-500">Host Crop:</span>
                                        <span class="ml-1 px-2 py-0.5 rounded-md bg-emerald-700 text-white font-semibold">${diag.crop}</span>
                                    </div>
                                    <div>
                                        <span class="text-slate-500">Confidence:</span>
                                        <span class="ml-1 font-mono-tech font-extrabold text-emerald-700 text-sm">${diag.confidence}%</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Differential Diagnosis Candidates -->
                            <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80">
                                <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-2">
                                    Top-3 Differential Diagnosis Distribution
                                </div>
                                ${diffRowsHtml}
                            </div>
                        </div>

                        <div class="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                            <span>🔍 Key Symptom Match</span>
                            <span class="font-semibold text-emerald-700">Validated • ICAR Reference</span>
                        </div>
                    </div>
                </div>

                <!-- CLINICAL AGRONOMIC ACTION PLAN (PRESCRIPTION PAD) -->
                <div class="rx-ribbon p-6">
                    <div class="flex flex-wrap items-center justify-between gap-4 pb-4 mb-5 border-b border-emerald-200/80">
                        <div class="flex items-center gap-3.5">
                            <div class="w-11 h-11 rounded-2xl bg-emerald-700 text-white flex items-center justify-center text-xl font-extrabold shadow-sm">
                                ℞
                            </div>
                            <div>
                                <h3 class="text-lg font-extrabold text-slate-900 tracking-tight">${window.t("rx_header")}</h3>
                                <p class="text-xs text-emerald-800 font-medium">${window.t("rx_sub")}</p>
                            </div>
                        </div>
                        <div class="flex flex-wrap items-center gap-3 text-xs">
                            <div class="px-3 py-1.5 rounded-xl bg-white border border-slate-200 shadow-2xs">
                                <span class="text-slate-400 font-medium">Rx ID:</span>
                                <span class="font-mono-tech font-bold text-slate-800 ml-1">#${diag.rx_id}</span>
                            </div>
                            <button type="button" onclick="window.AppController.switchTab('report')" class="btn-white text-xs py-2 px-3.5">
                                📄 Open Formal Report & PDF
                            </button>
                        </div>
                    </div>

                    <!-- Symptoms Banner -->
                    <div class="p-3.5 rounded-xl bg-white/90 border border-slate-200/90 mb-4 flex items-start gap-3">
                        <span class="text-base mt-0.5">🔬</span>
                        <div class="text-xs leading-relaxed text-slate-700">
                            <strong class="text-slate-900">Observed Pathological Morphology:</strong>
                            <span id="rx-symptoms-text">${diag.treatment.symptoms}</span>
                        </div>
                    </div>

                    <!-- 4-Column Decision Support Grid -->
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        <!-- Pesticide -->
                        <div class="bg-white p-4 rounded-xl border border-slate-200/90 shadow-2xs flex flex-col justify-between">
                            <div>
                                <div class="flex items-center gap-2 text-xs font-bold text-emerald-800 uppercase tracking-wider mb-2">
                                    <span class="w-6 h-6 rounded-lg bg-emerald-50 border border-emerald-200 flex items-center justify-center text-sm">🛡️</span>
                                    <span>${window.t("pesticide_title")}</span>
                                </div>
                                <p id="rx-pesticide-text" class="text-xs text-slate-700 leading-relaxed">${diag.treatment.pesticide}</p>
                            </div>
                            <div class="mt-3 pt-2 border-t border-slate-100 text-[11px] text-slate-400 font-medium">
                                Curative & Protective Regimen
                            </div>
                        </div>

                        <!-- Fertilizer -->
                        <div class="bg-white p-4 rounded-xl border border-slate-200/90 shadow-2xs flex flex-col justify-between">
                            <div>
                                <div class="flex items-center gap-2 text-xs font-bold text-emerald-800 uppercase tracking-wider mb-2">
                                    <span class="w-6 h-6 rounded-lg bg-emerald-50 border border-emerald-200 flex items-center justify-center text-sm">🌱</span>
                                    <span>${window.t("fertilizer_title")}</span>
                                </div>
                                <p id="rx-fertilizer-text" class="text-xs text-slate-700 leading-relaxed">${diag.treatment.fertilizer}</p>
                            </div>
                            <div class="mt-3 pt-2 border-t border-slate-100 text-[11px] text-slate-400 font-medium">
                                Physiological Immunity Boost
                            </div>
                        </div>

                        <!-- Market Impact Analysis (Architecture Box #16) -->
                        <div class="bg-white p-4 rounded-xl border border-slate-200/90 shadow-2xs flex flex-col justify-between">
                            <div>
                                <div class="flex items-center gap-2 text-xs font-bold text-sky-800 uppercase tracking-wider mb-2">
                                    <span class="w-6 h-6 rounded-lg bg-sky-50 border border-sky-200 flex items-center justify-center text-sm">📈</span>
                                    <span>${window.t("market_title")}</span>
                                </div>
                                <p id="rx-market-text" class="text-xs text-slate-700 leading-relaxed">${diag.treatment.market_impact}</p>
                            </div>
                            <div class="mt-3 pt-2 border-t border-slate-100 text-[11px] text-sky-600 font-semibold">
                                Economic & Yield Protection
                            </div>
                        </div>

                        <!-- Voice TTS Readout -->
                        <div class="bg-white p-4 rounded-xl border border-slate-200/90 shadow-2xs flex flex-col justify-between">
                            <div>
                                <div class="flex items-center gap-2 text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">
                                    <span class="w-6 h-6 rounded-lg bg-slate-100 border border-slate-200 flex items-center justify-center text-sm">🔊</span>
                                    <span>${window.t("tts_title")}</span>
                                </div>
                                <p class="text-xs text-slate-500 leading-relaxed mb-3">
                                    Synthesize spoken agronomic advisory in <b class="text-slate-800">${window.AppState.langName}</b> for field accessibility.
                                </p>
                                <button id="btn-tts-play" type="button" onclick="window.DiagnosisSection.playPrescriptionAudio()" class="btn-emerald w-full text-xs py-2.5">
                                    ▶️ <span>${window.t("btn_play_tts")}</span>
                                </button>
                                <div id="tts-audio-holder"></div>
                            </div>
                            <div class="mt-3 pt-2 border-t border-slate-100 text-[11px] text-slate-400 font-medium">
                                Google gTTS Neural Synthesizer
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
};
