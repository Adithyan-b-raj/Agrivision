/**
 * AgriVision Pro — Master SPA State & Navigation Controller
 * Enforces standalone /login page authentication and orchestrates the 4 clinical views.
 */

window.AppState = {
    loggedIn: false,
    user: null,
    lang: "en",
    langName: "English",
    activeTab: "diagnosis",
    lastDiagnosis: null,
    telemetry: null
};

window.AppController = {
    async init() {
        // 1. Check URL for Google OAuth 2.0 callback (?code=...) landing on root "/"
        const urlParams = new URLSearchParams(window.location.search);
        const oauthCode = urlParams.get("code");
        const oauthError = urlParams.get("error");

        if (oauthError) {
            window.location.replace(`/login?error=${encodeURIComponent(oauthError)}`);
            return;
        }

        if (oauthCode) {
            window.history.replaceState({}, document.title, window.location.pathname);
            try {
                const origin = window.location.origin;
                const res = await window.AgriAPI.exchangeGoogleCode(oauthCode, origin);
                if (res.logged_in && res.user) {
                    const serialized = JSON.stringify(res.user);
                    sessionStorage.setItem("agrivision_user", serialized);
                    localStorage.setItem("agrivision_user", serialized);
                }
            } catch (err) {
                window.location.replace(`/login?error=${encodeURIComponent(err.message)}`);
                return;
            }
        }

        // 2. Verify authenticated session; if not logged in, redirect to dedicated /login page
        const savedUser = sessionStorage.getItem("agrivision_user") || localStorage.getItem("agrivision_user");
        if (!savedUser) {
            window.location.replace("/login");
            return;
        }

        try {
            window.AppState.user = JSON.parse(savedUser);
            window.AppState.loggedIn = true;
            sessionStorage.setItem("agrivision_user", savedUser);
        } catch (e) {
            sessionStorage.removeItem("agrivision_user");
            localStorage.removeItem("agrivision_user");
            window.location.replace("/login");
            return;
        }

        this.renderUserBadge();

        // 3. Load system telemetry
        try {
            const telemetry = await window.AgriAPI.getTelemetry();
            window.AppState.telemetry = telemetry;
            this.updateHeaderTelemetry(telemetry);
            window.BenchmarkSection.render(telemetry);
        } catch (err) {
            console.warn("Initial telemetry load notice:", err);
        }

        // 4. Initialize section controllers
        window.DiagnosisSection.init();
        window.VoiceSection.init();
        window.ReportSection.renderReportView();

        // 5. Bind language selector
        const langSelect = document.getElementById("lang-selector");
        if (langSelect) {
            langSelect.addEventListener("change", (e) => {
                const code = e.target.value;
                const name = e.target.options[e.target.selectedIndex].text;
                this.setLanguage(code, name);
            });
        }
    },

    logout() {
        window.AppState.loggedIn = false;
        window.AppState.user = null;
        sessionStorage.removeItem("agrivision_user");
        localStorage.removeItem("agrivision_user");
        window.location.replace("/login");
    },

    renderUserBadge() {
        const user = window.AppState.user;
        const holder = document.getElementById("navbar-user-chip");
        if (!holder || !user) return;

        const avatarHtml =
            user.avatar && user.avatar.startsWith("http")
                ? `<img src="${user.avatar}" class="w-7 h-7 shrink-0 rounded-full object-cover border border-emerald-300" alt="${user.name}" />`
                : `<div class="w-7 h-7 shrink-0 rounded-full bg-emerald-100 text-emerald-800 font-bold text-xs flex items-center justify-center border border-emerald-200">🔬</div>`;

        holder.innerHTML = `
            <div class="inline-flex items-center gap-2 pl-1.5 pr-2.5 py-1 rounded-full bg-slate-100/90 border border-slate-200/90 max-w-full">
                ${avatarHtml}
                <div class="hidden sm:block text-left leading-tight min-w-0 max-w-[155px]">
                    <div class="text-xs font-bold text-slate-800 truncate">${user.name}</div>
                    <div class="text-[10px] text-emerald-700 font-medium truncate">${user.email}</div>
                </div>
                <button type="button" onclick="window.AppController.logout()" title="Sign Out to Login Page" class="ml-0.5 px-1.5 py-0.5 rounded-md hover:bg-red-50 text-xs text-slate-500 hover:text-red-600 font-semibold transition-colors shrink-0">
                    Sign Out
                </button>
            </div>
        `;
    },

    updateHeaderTelemetry(telemetry) {
        const el = document.getElementById("active-model-cls-count");
        if (el && telemetry.num_classes) {
            el.textContent = `${telemetry.num_classes} Classes`;
        }
    },

    switchTab(tabId) {
        window.AppState.activeTab = tabId;

        document.querySelectorAll(".nav-pill-btn").forEach((btn) => {
            btn.classList.toggle("active", btn.dataset.tab === tabId);
        });

        ["diagnosis", "voice", "benchmark", "report"].forEach((id) => {
            const sec = document.getElementById(`section-${id}`);
            if (sec) {
                sec.classList.toggle("hidden", id !== tabId);
            }
        });

        if (tabId === "report") {
            window.ReportSection.renderReportView();
        }
    },

    async setLanguage(langCode, langName) {
        window.AppState.lang = langCode;
        window.AppState.langName = langName;

        // Update all data-i18n elements immediately
        document.querySelectorAll("[data-i18n]").forEach((el) => {
            const key = el.getAttribute("data-i18n");
            el.textContent = window.t(key, langCode);
        });

        // If a diagnosis is currently active, translate its treatment strings smoothly
        if (window.AppState.lastDiagnosis) {
            const diag = window.AppState.lastDiagnosis;
            try {
                const tr = await window.AgriAPI.translatePrescription(diag.treatment.raw, langCode);
                diag.treatment.pesticide = tr.pesticide;
                diag.treatment.fertilizer = tr.fertilizer;
                diag.treatment.symptoms = tr.symptoms;
                diag.treatment.market_impact = tr.market_impact;
                window.DiagnosisSection.renderResults(diag);
                window.ReportSection.renderReportView();
            } catch (e) {
                console.warn("Live prescription translation error:", e);
            }
        }
    }
};

document.addEventListener("DOMContentLoaded", () => {
    window.AppController.init();
});
