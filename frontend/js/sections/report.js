/**
 * Section 4 Controller: AI-Generated Clinical Diagnostic Report Preview & PDF Export
 */

window.ReportSection = {
    async downloadPDF() {
        const diag = window.AppState.lastDiagnosis;
        if (!diag) return;

        const btn = document.getElementById("btn-download-pdf");
        const origHtml = btn ? btn.innerHTML : "";
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = `<span class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span> <span>Compiling PDF Report...</span>`;
        }

        try {
            const blob = await window.AgriAPI.downloadReportPDF(diag);
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `AgriVision_Report_${diag.disease.replace(/\s+/g, "_")}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
        } catch (err) {
            alert("Failed to generate PDF report: " + err.message);
        } finally {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = origHtml;
            }
        }
    },

    renderReportView() {
        const container = document.getElementById("report-content-area");
        if (!container) return;

        const diag = window.AppState.lastDiagnosis;
        const user = window.AppState.user || {
            name: "Dr. Clinical Pathologist",
            role: "Lead Diagnostic Evaluator",
            email: "agronomist@agrivision.ai"
        };

        if (!diag) {
            container.innerHTML = `
                <div class="studio-card p-10 text-center max-w-xl mx-auto my-6">
                    <div class="w-14 h-14 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-2xl mx-auto mb-4">
                        📄
                    </div>
                    <h4 class="text-base font-bold text-slate-900 mb-1">No Active Clinical Record Yet</h4>
                    <p class="text-xs text-slate-500 mb-5">${window.t("Please run a diagnosis on Tab 1 first to generate a report.")}</p>
                    <div class="flex items-center justify-center gap-3">
                        <button type="button" onclick="window.AppController.switchTab('diagnosis')" class="btn-white text-xs">
                            🔬 Go to Live Diagnosis
                        </button>
                        <button type="button" onclick="window.AppController.switchTab('diagnosis'); window.DiagnosisSection.handleSampleRun();" class="btn-emerald text-xs">
                            🌿 Run Sample Leaf & Generate Report
                        </button>
                    </div>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start section-fade">
                <!-- Left Column: Live Clinical Sheet Preview (8 cols) -->
                <div class="lg:col-span-8 studio-card p-8 bg-white border-slate-200 shadow-md">
                    <!-- Official Letterhead -->
                    <div class="flex flex-wrap items-start justify-between gap-4 pb-5 border-b-2 border-emerald-700">
                        <div class="flex items-center gap-3.5">
                            <div class="w-12 h-12 rounded-2xl bg-emerald-700 text-white flex items-center justify-center text-2xl shadow-xs">
                                🌿
                            </div>
                            <div>
                                <div class="text-xs font-bold uppercase tracking-widest text-emerald-700">AgriVision AI • Clinical Pathology Record</div>
                                <h3 class="text-xl font-extrabold text-slate-900">Plant Health & Diagnostic Prescription Sheet</h3>
                                <div class="text-xs text-slate-500">Department of Computer Science & Engineering • STIST Trivandrum</div>
                            </div>
                        </div>
                        <div class="text-right font-mono-tech text-xs text-slate-600 bg-slate-50 px-3.5 py-2 rounded-xl border border-slate-200">
                            <div><b>Record ID:</b> #${diag.rx_id}</div>
                            <div><b>Date:</b> ${diag.timestamp}</div>
                            <div><b>Status:</b> <span class="text-emerald-700 font-bold">VALIDATED</span></div>
                        </div>
                    </div>

                    <!-- Patient / Specimen Metadata Strip -->
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 my-5 p-4 rounded-xl bg-slate-50 border border-slate-200/80 text-xs">
                        <div>
                            <div class="text-[10px] font-bold uppercase text-slate-400">Identified Disease</div>
                            <div class="font-extrabold text-slate-900 text-sm mt-0.5">${diag.disease}</div>
                        </div>
                        <div>
                            <div class="text-[10px] font-bold uppercase text-slate-400">Host Crop Species</div>
                            <div class="font-bold text-emerald-700 text-sm mt-0.5">${diag.crop}</div>
                        </div>
                        <div>
                            <div class="text-[10px] font-bold uppercase text-slate-400">Confidence / Severity</div>
                            <div class="font-bold text-slate-900 text-sm mt-0.5 font-mono-tech">${diag.confidence}% • ${diag.severity.label}</div>
                        </div>
                        <div>
                            <div class="text-[10px] font-bold uppercase text-slate-400">Reviewing Specialist</div>
                            <div class="font-bold text-slate-800 text-sm mt-0.5">${user.name}</div>
                        </div>
                    </div>

                    <!-- 3-Stage Visual Evidence Strip -->
                    <div class="mb-6">
                        <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2.5">Multimodal Visual Evidence</div>
                        <div class="grid grid-cols-3 gap-3">
                            <div class="rounded-xl overflow-hidden border border-slate-200 bg-slate-950">
                                <img src="${diag.images.detection}" class="w-full h-36 object-cover" alt="Detection" />
                                <div class="bg-white px-2.5 py-1.5 text-[11px] font-semibold text-slate-700 border-t border-slate-200">
                                    1. RT-DETR (${diag.num_lesions} Spots)
                                </div>
                            </div>
                            <div class="rounded-xl overflow-hidden border border-slate-200 bg-slate-950">
                                <img src="${diag.images.segmentation}" class="w-full h-36 object-cover" alt="SAM 2 Mask" />
                                <div class="bg-white px-2.5 py-1.5 text-[11px] font-semibold text-slate-700 border-t border-slate-200">
                                    2. SAM-2 Mask (${diag.infected_area_pct}% Area)
                                </div>
                            </div>
                            <div class="rounded-xl overflow-hidden border border-slate-200 bg-slate-950">
                                <img src="${diag.images.gradcam}" class="w-full h-36 object-cover" alt="Grad-CAM++" />
                                <div class="bg-white px-2.5 py-1.5 text-[11px] font-semibold text-slate-700 border-t border-slate-200">
                                    3. Grad-CAM++ Attention
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Clinical Findings & Treatment Protocol -->
                    <div class="space-y-3 text-xs">
                        <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80">
                            <div class="font-bold text-slate-900 mb-1">🔬 Key Symptoms & Morphological Findings</div>
                            <div class="text-slate-600 leading-relaxed">${diag.treatment.symptoms}</div>
                        </div>
                        <div class="p-3.5 rounded-xl bg-emerald-50/50 border border-emerald-200/80">
                            <div class="font-bold text-emerald-900 mb-1">🛡️ Curative Pesticide & Fungicide Regimen</div>
                            <div class="text-slate-700 leading-relaxed">${diag.treatment.pesticide}</div>
                        </div>
                        <div class="p-3.5 rounded-xl bg-emerald-50/50 border border-emerald-200/80">
                            <div class="font-bold text-emerald-900 mb-1">🌱 Bio-Fertilizer & Soil Nutrient Protocol</div>
                            <div class="text-slate-700 leading-relaxed">${diag.treatment.fertilizer}</div>
                        </div>
                    </div>
                </div>

                <!-- Right Column: Export Actions & Metadata (4 cols) -->
                <div class="lg:col-span-4 space-y-4">
                    <div class="studio-card p-6">
                        <div class="flex items-center gap-3 mb-3">
                            <div class="w-10 h-10 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-lg">
                                📥
                            </div>
                            <div>
                                <h4 class="text-base font-bold text-slate-900">Instant Report Export</h4>
                                <p class="text-xs text-slate-500">Compiled via FPDF2 Clinical Engine</p>
                            </div>
                        </div>

                        <p class="text-xs text-slate-600 leading-relaxed mb-5">
                            Download a high-resolution, print-ready PDF containing the annotated leaf specimen, severity metrics, and official agronomic prescription.
                        </p>

                        <button id="btn-download-pdf" type="button" onclick="window.ReportSection.downloadPDF()" class="btn-emerald w-full py-3 text-sm mb-3">
                            ⬇️ <span>${window.t("btn_download_pdf")}</span>
                        </button>

                        <button type="button" onclick="window.print()" class="btn-white w-full py-2.5 text-xs">
                            🖨️ Print Clinical Record Sheet
                        </button>

                        <div class="mt-5 pt-4 border-t border-slate-100 space-y-2 text-xs text-slate-500">
                            <div class="flex justify-between">
                                <span>Format:</span>
                                <span class="font-semibold text-slate-700">A4 Portrait PDF (FPDF2)</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Neural Backbone:</span>
                                <span class="font-semibold text-slate-700">ConvNeXt V2 + SAM 2.1</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Verification:</span>
                                <span class="font-semibold text-emerald-700">✓ Digital Lab Stamp</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
};
