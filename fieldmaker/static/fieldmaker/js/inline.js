(function($) {
    $(document).ready(function() {
        inline_add = function (row) {
            console.log(['row added', row])
            row.filter('.dynamic-set').each(register_dynamic_set);
            row.find('.dynamic-set').each(register_dynamic_set);
        }
        register_dynamic_set = function() {
            var $this = $(this);
            var prefix = $this.attr('data-prefix');
            if (!prefix) return;
            if ($this.data('dynamic_registered')) return;
            var rows = $this.children('table').children('tbody').children('.dynamic-form');
            if (!rows) return;
            
            var field_form = $this.find('.empty-form')
            field_form.find(':input').each(function() {
                var field_name = $(this).attr('name');
                $(this).attr('name', field_name.replace(/.*\-/, prefix+'-'));
                $(this).attr('id', 'id_'+$(this).attr('name'));
            });
            field_form.attr('id', prefix+'-empty');
            
            rows.formset({
                prefix: prefix,
                addText: "Add another Field Entry",
                formCssClass: "dynamic-form",
                deleteCssClass: "inline-deletelink",
                deleteText: "Remove",
                emptyCssClass: "empty-form",
                added: inline_add
            });
            $this.data('dynamic_registered', true)
            
        }
        $('.dynamic-set').each(register_dynamic_set);
    });
})(django.jQuery);

