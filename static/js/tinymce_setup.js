(function ($) {
    "use strict";

    function initTinyFor(el) {
        var id = el.id;
        if (!id) return;
        if (tinymce.get(id)) return;
        tinymce.init({
            selector: '#' + id,
            menubar: false,
            toolbar: 'undo redo | styleselect | bold italic | bullist numlist | link',
            height: 250,
            // add more TinyMCE config here if needed
            setup: function (editor) {
                // If this is the empty inline template (prefix), remove the instance
                editor.on('init', function () {
                    var $el = $(editor.getElement());
                    if ($el.closest('.empty-form, .inline-empty-form').length || (editor.id && editor.id.indexOf('__prefix__') !== -1)) {
                        editor.remove();
                    }
                });
            }
        });
    }

    $(function () {
        // initialize existing textareas (exclude the empty form)
        $('textarea').each(function () {
            var $t = $(this);
            if ($t.closest('.empty-form, .inline-empty-form').length) return;
            initTinyFor(this);
        });

        // when a new inline row is added (Django formset event)
        $(document).on('formset:added', function (event, $row) {
            $row.find('textarea').each(function () { initTinyFor(this); });
        });

        // when an inline row is removed, clean up TinyMCE instances
        $(document).on('formset:removed', function (event, $row) {
            $row.find('textarea').each(function () {
                var id = this.id;
                if (id && tinymce.get(id)) tinymce.get(id).remove();
            });
        });
    });
})(window.django && window.django.jQuery ? window.django.jQuery : window.jQuery);