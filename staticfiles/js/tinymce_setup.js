(function ($) {
    "use strict";

    function initTiny(el) {
        if (!el || !el.id) return;
        if (typeof tinymce === "undefined") return;
        if (tinymce.get(el.id)) return;
        console.debug("initTiny:", el.id);
        tinymce.init({
            selector: "#" + el.id,
            menubar: false,
            plugins: ["lists", "link", "paste"],   // use array to avoid combined-name requests
            toolbar: "undo redo | formatselect | bold italic | bullist numlist | link",
            height: 280,
            branding: false,
            inline: false
        });
    }

    function removeTiny(el) {
        if (!el || !el.id) return;
        if (typeof tinymce === "undefined") return;
        var inst = tinymce.get(el.id);
        if (inst) inst.remove();
    }

    function initAllTextareas() {
        var $areas = $("textarea.tinymce");
        if (!$areas.length) {
            $areas = $("textarea").not(".vHidden, .hidden, .inline-empty-form textarea");
        }
        $areas.each(function () {
            var $t = $(this);
            if ($t.closest(".empty-form, .inline-empty-form").length) return;
            if (this.id && this.id.indexOf("__prefix__") === -1) initTiny(this);
        });
    }

    function waitForTinyAndInit(timeoutMs) {
        var waited = 0, interval = 50, max = timeoutMs || 5000;
        var iv = setInterval(function () {
            if (typeof tinymce !== "undefined") {
                clearInterval(iv);
                initAllTextareas();
                return;
            }
            waited += interval;
            if (waited >= max) {
                clearInterval(iv);
                initAllTextareas();
            }
        }, interval);
    }

    $(function () {
        if (typeof tinymce !== "undefined") {
            initAllTextareas();
        } else {
            waitForTinyAndInit(5000);
        }

        $(document).on("formset:added inline:added", function (e, $row) {
            var $r = $row && $row.length ? $row : $(e.target);
            $r.find("textarea.tinymce").each(function () { initTiny(this); });
        });

        $(document).on("formset:removed inline:removed", function (e, $row) {
            var $r = $row && $row.length ? $row : $(e.target);
            $r.find("textarea.tinymce").each(function () { removeTiny(this); });
        });
    });
})(window.django && window.django.jQuery ? window.django.jQuery : window.jQuery);