(function () {
    "use strict";

    var INTRO_JS_CDN = "https://cdn.jsdelivr.net/npm/intro.js/minified/intro.min.js";

    function q(selector) { try { return document.querySelector(selector); } catch (e) { return null; } }
    function exists(selector) { return !!q(selector); }

    function loadScript(url, cb) {
        var s = document.createElement("script");
        s.src = url;
        s.async = true;
        s.onload = function () { if (cb) cb(null); };
        s.onerror = function () { if (cb) cb(new Error("Failed to load " + url)); };
        document.head.appendChild(s);
    }

    function ensureIntroJs(ready) {
        if (typeof introJs === "function") return ready();
        loadScript(INTRO_JS_CDN, function (err) {
            if (err) console.error(err);
            ready();
        });
    }

    function buildSteps() {
        var steps = [];

        if (exists("#grp-content-title header h1")) {
            steps.push({ element: "#grp-content-title header h1", intro: "Welcome to the Edu‑flow Dashboard." });
        } else if (exists("header h1")) {
            steps.push({ element: "header h1", intro: "Welcome to the Edu‑flow Dashboard." });
        }

        if (exists('#grp-user-tools a[href="/"]')) {
            steps.push({ element: '#grp-user-tools a[href="/"]', intro: 'Go to the public site (Home).' });
        } else if (exists('#user-tools a[href="/"]')) {
            steps.push({ element: '#user-tools a[href="/"]', intro: 'Go to the public site (Home).' });
        }

        if (exists("#content-main .module") || exists(".dashboard-module")) {
            steps.push({ element: "#content-main .module, .dashboard-module", intro: "Dashboard panels and quick links." });
        }

        if (exists(".changelist") || exists("#changelist") || exists(".change-list")) {
            if (exists(".changelist .search-container") || exists(".search-form")) {
                steps.push({ element: ".changelist .search-container, .search-form", intro: "Use search to find items quickly." });
            }
            steps.push({ element: ".change-list, table", intro: "This is the list view. Use filters and pagination to navigate." });
        }

        if (exists("#content-main form") || exists("form")) {
            if (exists(".submit-row")) {
                steps.push({ element: ".submit-row", intro: "Use these buttons to save or cancel." });
            }
            steps.push({ element: "#content-main form, form", intro: "Edit the object here." });
        }

        if (!steps.length) steps.push({ element: "body", intro: "This is the admin area." });

        return steps;
    }

    function startTour(auto) {
        ensureIntroJs(function () {
            if (typeof introJs !== "function") {
                console.warn("introJs not available");
                return;
            }
            var raw = buildSteps();
            if (!raw || !raw.length) {
                if (!auto) alert("Tour not available on this page.");
                return;
            }
            var steps = raw.map(function (s) { return { element: s.element, intro: s.intro }; });
            introJs().setOptions({
                steps: steps,
                showProgress: true,
                exitOnOverlayClick: true,
                tooltipPosition: "auto"
            }).start();
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        console.log("admin_tour.js loaded (autostart mode)");

        // Auto-start once on dashboard only (no manual button)
        try {
            var shown = localStorage.getItem("eduflow_admin_tour_shown");
            var isDashboard = !!(q("#grp-content-title header h1") || q("header h1")) && !q(".changelist") && !q("form");
            if (!shown && isDashboard) {
                // small delay to ensure elements rendered
                setTimeout(function () {
                    startTour(true);
                    try { localStorage.setItem("eduflow_admin_tour_shown", "1"); } catch (e) { }
                }, 700);
            }
        } catch (e) { console.warn(e); }
    });

})();