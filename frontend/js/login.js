/**
 * AgriVision Pro — Dedicated Login Page Controller (/login)
 */

window.LoginController = {
    authConfig: null,

    async init() {
        // 1. Check if already authenticated
        const existingUser = sessionStorage.getItem("agrivision_user") || localStorage.getItem("agrivision_user");
        if (existingUser) {
            sessionStorage.setItem("agrivision_user", existingUser);
            window.location.replace("/");
            return;
        }

        // 2. Check URL for Google OAuth 2.0 callback (?code=...)
        const urlParams = new URLSearchParams(window.location.search);
        const oauthCode = urlParams.get("code");
        const oauthError = urlParams.get("error");

        if (oauthError) {
            window.history.replaceState({}, document.title, window.location.pathname);
            this.showError(`Google Sign-In was cancelled or declined (${oauthError}).`);
        } else if (oauthCode) {
            window.history.replaceState({}, document.title, window.location.pathname);
            await this.handleGoogleCallback(oauthCode);
            return;
        }

        // 3. Load Google OAuth & Workstation credentials configuration from backend (.env)
        try {
            this.authConfig = await window.AgriAPI.getAuthConfig();
            if (this.authConfig && this.authConfig.credentials) {
                const creds = this.authConfig.credentials;
                const emailInput = document.getElementById("login-email");
                const pwdInput = document.getElementById("login-password");
                if (emailInput && creds.email) {
                    emailInput.value = creds.email;
                }
                if (pwdInput && creds.default_password) {
                    pwdInput.value = creds.default_password;
                }
            }
        } catch (err) {
            console.warn("Auth config load notice:", err);
        }

        // 4. Bind UI Events
        const googleBtn = document.getElementById("btn-google-sso");
        const form = document.getElementById("clinical-login-form");
        const pwdToggle = document.getElementById("btn-toggle-pwd");
        const evalBtn = document.getElementById("btn-quick-evaluator");

        if (googleBtn) {
            googleBtn.addEventListener("click", () => this.startGoogleSignIn());
        }

        if (form) {
            form.addEventListener("submit", (e) => {
                e.preventDefault();
                this.submitCredentials();
            });
        }

        if (pwdToggle) {
            pwdToggle.addEventListener("click", () => {
                const pwdInput = document.getElementById("login-password");
                if (!pwdInput) return;
                if (pwdInput.type === "password") {
                    pwdInput.type = "text";
                    pwdToggle.textContent = "Hide password";
                } else {
                    pwdInput.type = "password";
                    pwdToggle.textContent = "Show password";
                }
            });
        }

        if (evalBtn) {
            evalBtn.addEventListener("click", () => this.loginEvaluator());
        }
    },

    showError(msg) {
        const banner = document.getElementById("login-error-banner");
        const text = document.getElementById("login-error-text");
        if (banner && text) {
            text.textContent = msg;
            banner.classList.remove("hidden");
        }
    },

    hideError() {
        const banner = document.getElementById("login-error-banner");
        if (banner) banner.classList.add("hidden");
    },

    async startGoogleSignIn() {
        this.hideError();
        try {
            this.authConfig = await window.AgriAPI.getAuthConfig();
        } catch (err) {
            console.warn("Auth config refresh error:", err);
        }
        if (this.authConfig && this.authConfig.configured && this.authConfig.auth_url) {
            window.location.href = this.authConfig.auth_url;
        } else {
            this.showError(
                "Google OAuth Client ID & Secret are not configured in .env yet. Please sign in using the Clinical Credentials form below or click 'Launch Demo'."
            );
        }
    },

    async handleGoogleCallback(code) {
        const submitBtn = document.getElementById("btn-submit-credentials");
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `<span class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span> <span>Verifying Google Identity...</span>`;
        }
        try {
            const origin = window.location.origin;
            const res = await window.AgriAPI.exchangeGoogleCode(code, origin);
            if (res.logged_in && res.user) {
                this.saveAndRedirect(res.user, true);
            }
        } catch (err) {
            this.showError(err.message);
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = `<span>Sign In to Clinical Workstation</span> <span>➔</span>`;
            }
        }
    },

    async submitCredentials() {
        this.hideError();
        const emailEl = document.getElementById("login-email");
        const pwdEl = document.getElementById("login-password");
        const rememberEl = document.getElementById("login-remember");
        const submitBtn = document.getElementById("btn-submit-credentials");

        const email = emailEl ? emailEl.value.trim() : "";
        const password = pwdEl ? pwdEl.value : "";
        const remember = rememberEl ? rememberEl.checked : true;

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `<span class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span> <span>Authenticating...</span>`;
        }

        try {
            const res = await window.AgriAPI.credentialsLogin(email, password);
            if (res.logged_in && res.user) {
                this.saveAndRedirect(res.user, remember);
            }
        } catch (err) {
            this.showError(err.message);
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = `<span>Sign In to Clinical Workstation</span> <span>➔</span>`;
            }
        }
    },

    async loginEvaluator() {
        this.hideError();
        try {
            const res = await window.AgriAPI.offlineLogin();
            if (res.logged_in && res.user) {
                this.saveAndRedirect(res.user, true);
            }
        } catch (err) {
            this.showError(err.message);
        }
    },

    saveAndRedirect(userObj, remember = true) {
        const serialized = JSON.stringify(userObj);
        sessionStorage.setItem("agrivision_user", serialized);
        if (remember) {
            localStorage.setItem("agrivision_user", serialized);
        }
        window.location.replace("/");
    }
};

document.addEventListener("DOMContentLoaded", () => {
    window.LoginController.init();
});
