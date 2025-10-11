(function ($) {
    "use strict";

    function initTiny(el) {
        if (!el || !el.id) return;
        if (tinymce.get(el.id)) return;
        tinymce.init({
            selector: "#" + el.id,
            menubar: false,
            plugins: "lists link paste",
            toolbar: "undo redo | formatselect | bold italic | bullist numlist | link",
            height: 280,
            branding: false,
            // ensure toolbar visible above admin UI
            fixed_toolbar_container: null,
            // ensure not inline mode
            inline: false
        });
    }

    function removeTiny(el) {
        if (!el || !el.id) return;
        var inst = tinymce.get(el.id);
        if (inst) inst.remove();
    }

    $(function () {
        // init only textareas marked .tinymce and not the empty-form prefix
        $("textarea.tinymce").each(function () {
            var $t = $(this);
            if ($t.closest(".empty-form, .inline-empty-form").length) return;
            if (this.id && this.id.indexOf("__prefix__") === -1) initTiny(this);
        });

        // handle formset/add/remove events used by Django and Grappelli
        $(document).on("formset:added inline:added", function (e, $row) {
            // some events pass the row as second arg, some provide it in e.target
            var $r = $row && $row.length ? $row : $(e.target);
            $r.find("textarea.tinymce").each(function () { initTiny(this); });
        });

        $(document).on("formset:removed inline:removed", function (e, $row) {
            var $r = $row && $row.length ? $row : $(e.target);
            $r.find("textarea.tinymce").each(function () { removeTiny(this); });
        });
    });
})(window.django && window.django.jQuery ? window.django.jQuery : window.jQuery);