(function () {
    "use strict";

    var GRAPPELLI_TINYMCE = "/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js";
    var CONFIG = {
        selector: "textarea.tinymce",
        menubar: false,
        plugins: "link lists paste code",
        toolbar: "undo redo | bold italic | bullist numlist | link | code",
        branding: false,
        height: 300,
        paste_as_text: true,
        setup: function (editor) { editor.on("change", function () { editor.save(); }); }
    };

    function loadScript(url, cb) {
        var s = document.createElement("script");
        s.src = url;
        s.async = true;
        s.onload = function () { cb && cb(null); };
        s.onerror = function () { cb && cb(new Error("failed to load " + url)); };
        document.head.appendChild(s);
    }

    function ensureTiny(callback) {
        if (window.tinyMCE && typeof window.tinyMCE.init === "function") return callback();
        loadScript(GRAPPELLI_TINYMCE, function (err) {
            if (err) console.warn(err);
            callback();
        });
    }

    function initAll() {
        if (!window.tinyMCE) return;
        document.querySelectorAll("textarea.tinymce").forEach(function (ta) {
            if (ta.id && ta.id.indexOf("__prefix__") !== -1) return;
            if (!ta.id) ta.id = "ta_" + Math.random().toString(36).slice(2, 10);
            if (window.tinyMCE.get(ta.id)) return;
            var cfg = Object.assign({}, CONFIG, { target: ta });
            window.tinyMCE.init(cfg);
        });
    }

    function removeEditors(node) {
        if (!window.tinyMCE) return;
        (node.querySelectorAll ? node.querySelectorAll("textarea.tinymce") : []).forEach(function (ta) {
            if (ta.id && window.tinyMCE.get(ta.id)) {
                try { window.tinyMCE.get(ta.id).remove(); } catch (e) { }
            }
        });
    }

    function observeMutations() {
        var obs = new MutationObserver(function (mutations) {
            mutations.forEach(function (m) {
                (m.addedNodes || []).forEach(function (n) {
                    if (n.nodeType !== 1) return;
                    if (n.matches && n.matches("textarea.tinymce")) initAll();
                    else if (n.querySelector && n.querySelector("textarea.tinymce")) initAll();
                });
                (m.removedNodes || []).forEach(function (n) {
                    if (n.nodeType !== 1) return;
                    removeEditors(n);
                });
            });
        });
        obs.observe(document.body, { childList: true, subtree: true });
    }

    document.addEventListener("DOMContentLoaded", function () {
        ensureTiny(function () {
            initAll();
            observeMutations();
            document.addEventListener("submit", function () {
                try { window.tinyMCE && window.tinyMCE.triggerSave(); } catch (e) { }
            }, true);
        });
    });
})();