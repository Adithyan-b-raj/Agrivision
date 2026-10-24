/**
 * Section 3 Controller: Multiple Backbone Comparison & PlantSeg Benchmark Suite
 */

window.BenchmarkSection = {
    activeMetric: "top5_acc", // "top5_acc" | "top1_acc" | "latency_ms"

    render(telemetry) {
        const container = document.getElementById("benchmark-content-area");
        if (!container || !telemetry) return;

        const backbones = telemetry.backbones || [];

        const tableRows = backbones
            .map(
                (b) => `
            <tr class="${b.is_active ? "bg-emerald-50/70 font-semibold" : "hover:bg-slate-50/80"} transition-colors border-b border-slate-100 last:border-0">
                <td class="py-3.5 px-4">
                    <div class="flex items-center gap-2.5">
                        <span class="w-2.5 h-2.5 rounded-full ${b.is_active ? "bg-emerald-500" : "bg-slate-300"}"></span>
                        <div>
                            <div class="text-sm font-bold text-slate-900 flex items-center gap-2">
                                ${b.name}
                                ${b.is_active ? `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-600 text-white uppercase tracking-wider">Ours • Active</span>` : ""}
                            </div>
                            <div class="text-xs text-slate-500 font-normal">${b.family}</div>
                        </div>
                    </div>
                </td>
                <td class="py-3.5 px-4 font-mono-tech text-sm ${b.is_active ? "text-emerald-700 font-extrabold" : "text-slate-700"}">${b.top1_acc.toFixed(2)}%</td>
                <td class="py-3.5 px-4 font-mono-tech text-sm ${b.is_active ? "text-emerald-700 font-extrabold" : "text-slate-700"}">${b.top5_acc.toFixed(2)}%</td>
                <td class="py-3.5 px-4 font-mono-tech text-sm text-slate-600">${b.miou_mask.toFixed(2)}%</td>
                <td class="py-3.5 px-4 font-mono-tech text-sm text-slate-600">${b.params_m}M</td>
                <td class="py-3.5 px-4">
                    <span class="px-2.5 py-1 rounded-lg font-mono-tech text-xs font-bold ${b.is_active ? "bg-emerald-100 text-emerald-800 border border-emerald-200" : "bg-slate-100 text-slate-600"}">
                        ${b.latency_ms} ms ${b.is_active ? "⚡" : ""}
                    </span>
                </td>
            </tr>
        `
            )
            .join("");

        const chartBars = backbones
            .map((b) => {
                let val = b.top5_acc;
                let maxVal = 100;
                let unit = "%";
                let barColor = b.is_active ? "bg-emerald-600" : "bg-slate-400";

                if (this.activeMetric === "top1_acc") {
                    val = b.top1_acc;
                } else if (this.activeMetric === "latency_ms") {
                    val = b.latency_ms;
                    maxVal = 50;
                    unit = " ms";
                    barColor = b.is_active ? "bg-emerald-600" : "bg-amber-500";
                }

                const pctWidth = Math.min((val / maxVal) * 100, 100);
                return `
                    <div class="space-y-1.5">
                        <div class="flex items-center justify-between text-xs">
                            <span class="font-bold ${b.is_active ? "text-emerald-800" : "text-slate-700"}">${b.name}</span>
                            <span class="font-mono-tech font-bold ${b.is_active ? "text-emerald-700" : "text-slate-600"}">${val}${unit}</span>
                        </div>
                        <div class="w-full h-3 bg-slate-100 rounded-full overflow-hidden">
                            <div class="h-full ${barColor} rounded-full transition-all duration-700" style="width: ${pctWidth}%"></div>
                        </div>
                    </div>
                `;
            })
            .join("");

        container.innerHTML = `
            <div class="space-y-6 section-fade">
                <!-- 4 Hero Telemetry KPI Cards -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div class="studio-card studio-card-hover p-5">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Top-1 Accuracy</span>
                            <span class="w-8 h-8 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-sm">🏆</span>
                        </div>
                        <div class="text-3xl font-extrabold text-slate-900 font-mono-tech">80.80%</div>
                        <div class="mt-2 inline-flex items-center gap-1 text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md">
                            ↑ +1.40% vs DINOv2 Baseline
                        </div>
                    </div>

                    <div class="studio-card studio-card-hover p-5">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Top-5 Diagnostic</span>
                            <span class="w-8 h-8 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-sm">🌟</span>
                        </div>
                        <div class="text-3xl font-extrabold text-emerald-700 font-mono-tech">97.21%</div>
                        <div class="mt-2 inline-flex items-center gap-1 text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md">
                            Clinical Safety Standard (>95%)
                        </div>
                    </div>

                    <div class="studio-card studio-card-hover p-5">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Inference Latency</span>
                            <span class="w-8 h-8 rounded-xl bg-sky-50 border border-sky-200 flex items-center justify-center text-sm">⚡</span>
                        </div>
                        <div class="text-3xl font-extrabold text-slate-900 font-mono-tech">14.2 ms</div>
                        <div class="mt-2 inline-flex items-center gap-1 text-xs font-semibold text-sky-700 bg-sky-50 px-2 py-0.5 rounded-md">
                            3.0x Faster than Vision Transformers
                        </div>
                    </div>

                    <div class="studio-card studio-card-hover p-5">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold uppercase tracking-wider text-slate-400">PlantSeg Coverage</span>
                            <span class="w-8 h-8 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-center text-sm">🌿</span>
                        </div>
                        <div class="text-3xl font-extrabold text-slate-900 font-mono-tech">115 Classes</div>
                        <div class="mt-2 inline-flex items-center gap-1 text-xs font-semibold text-amber-800 bg-amber-50 px-2 py-0.5 rounded-md">
                            11,400+ In-the-Wild Specimens
                        </div>
                    </div>
                </div>

                <!-- Comparative Matrix + Interactive Chart Split -->
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                    <!-- Table (7 cols) -->
                    <div class="lg:col-span-7 studio-card p-6 overflow-hidden">
                        <div class="flex items-center justify-between mb-4">
                            <div>
                                <h4 class="text-base font-bold text-slate-900">Comparative Backbone Matrix</h4>
                                <p class="text-xs text-slate-500">Architecture Diagram Box #4 & #10: ConvNeXt V2 vs Vision Transformers</p>
                            </div>
                            <span class="px-2.5 py-1 rounded-lg text-xs font-mono-tech font-semibold bg-slate-100 text-slate-700">
                                Tesla P100 FP16
                            </span>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left border-collapse">
                                <thead>
                                    <tr class="border-b border-slate-200 text-[11px] font-bold uppercase tracking-wider text-slate-400">
                                        <th class="py-2.5 px-4">Backbone Architecture</th>
                                        <th class="py-2.5 px-4">Top-1</th>
                                        <th class="py-2.5 px-4">Top-5</th>
                                        <th class="py-2.5 px-4">mIoU</th>
                                        <th class="py-2.5 px-4">Params</th>
                                        <th class="py-2.5 px-4">Latency</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${tableRows}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Interactive Visual Chart (5 cols) -->
                    <div class="lg:col-span-5 studio-card p-6 flex flex-col justify-between">
                        <div>
                            <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
                                <h4 class="text-base font-bold text-slate-900">Visual Telemetry Breakdown</h4>
                                <div class="seg-control">
                                    <button type="button" onclick="window.BenchmarkSection.switchMetric('top5_acc')" class="seg-btn ${this.activeMetric === "top5_acc" ? "active" : ""}">Top-5 %</button>
                                    <button type="button" onclick="window.BenchmarkSection.switchMetric('top1_acc')" class="seg-btn ${this.activeMetric === "top1_acc" ? "active" : ""}">Top-1 %</button>
                                    <button type="button" onclick="window.BenchmarkSection.switchMetric('latency_ms')" class="seg-btn ${this.activeMetric === "latency_ms" ? "active" : ""}">Latency</button>
                                </div>
                            </div>
                            <div class="space-y-4 mt-4">
                                ${chartBars}
                            </div>
                        </div>

                        <div class="mt-6 p-4 rounded-xl bg-emerald-50/70 border border-emerald-200/80 text-xs text-slate-700 leading-relaxed">
                            <div class="font-bold text-emerald-900 mb-1">🧬 Architectural Rationale & Clinical Justification</div>
                            While heavy Vision Transformers (DINOv2, EVA-02) require 86M+ parameters, <b>ConvNeXt V2 (Tiny)</b> with Global Response Normalization (GRN) achieves the highest clinical diagnostic accuracy (<b>80.80% Top-1 / 97.21% Top-5</b>) at <b>28.6M parameters</b> and <b>14.2 ms latency</b>—retaining sharp 7×7 depthwise lesion boundaries.
                        </div>
                    </div>
                </div>
            </div>
        `;
    },

    switchMetric(metricKey) {
        this.activeMetric = metricKey;
        if (window.AppState.telemetry) {
            this.render(window.AppState.telemetry);
        }
    }
};
