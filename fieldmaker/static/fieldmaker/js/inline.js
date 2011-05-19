(function($) {
    $(document).ready(function() {
        register_dynamic_set = function() {
            var $this = $(this);
            var prefix = $this.attr('data-prefix');
            if (!prefix) return;
            var rows = $this.children('table').children('tbody').children('.dynamic-form');
            if (!rows) return;
            rows.formset({
                prefix: prefix,
                addText: "Add another Field Entry",
                formCssClass: "dynamic-form",
                deleteCssClass: "inline-deletelink",
                deleteText: "Remove",
                emptyCssClass: "empty-form"
            });
        }
        $('.dynamic-set').each(register_dynamic_set);
    });
})(django.jQuery);

