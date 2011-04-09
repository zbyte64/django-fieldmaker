from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.forms.formsets import formset_factory

from models import FormDefinition, GenericObjectStore
from forms import FieldEntryForm, BaseFieldEntryFormSet

class FieldEntryInlineAdmin(BaseModelAdmin):
    """
    Options for inline editing of ``model`` instances.

    Provide ``name`` to specify the attribute name of the ``ForeignKey`` from
    ``model`` to its parent. This is required if ``model`` has more than one
    ``ForeignKey`` to its parent.
    """
    #formset = FieldEntryFormSet
    extra = 1
    max_num = None
    template = 'admin/fieldmaker/fieldentry_stacked.html'
    verbose_name = None
    verbose_name_plural = None
    can_delete = True
    model = FormDefinition #django doesn't like have non-model inlines
    fk_name = None
    verbose_name = 'Field Entry'
    verbose_name_plural = 'Field Entries'

    def __init__(self, parent_model, admin_site, *args, **kwargs):
        self.admin_site = admin_site
        self.parent_model = parent_model
        super(FieldEntryInlineAdmin, self).__init__(*args, **kwargs)
    
    def get_queryset(self, request=None):
        return None

    def _media(self):
        from django.conf import settings
        from django.forms import Media
        js = ['js/jquery.min.js', 'js/jquery.init.js', 'js/inlines.min.js']
        if self.prepopulated_fields:
            js.append('js/urlify.js')
            js.append('js/prepopulate.min.js')
        if self.filter_vertical or self.filter_horizontal:
            js.extend(['js/SelectBox.js' , 'js/SelectFilter2.js'])
        return Media(js=['%s%s' % (settings.ADMIN_MEDIA_PREFIX, url) for url in js])
    media = property(_media)

    def get_formset(self, request, obj=None, **kwargs):
        """Returns a BaseInlineFormSet class for use in admin add/change views."""
        defaults = {
            "form": FieldEntryForm,
            "formset": BaseFieldEntryFormSet,
            "extra": self.extra,
            "max_num": self.max_num,
            "can_delete": self.can_delete,
        }
        defaults.update(kwargs)
        return formset_factory(**defaults)

    def get_fieldsets(self, request, obj=None):
        if self.declared_fieldsets:
            return self.declared_fieldsets
        form = self.get_formset(request).form
        fields = form.base_fields.keys() + list(self.get_readonly_fields(request, obj))
        return [(None, {'fields': fields})]

class FormDefinitionAdmin(admin.ModelAdmin):
    inlines = [FieldEntryInlineAdmin]
    #exclude = ['data']

admin.site.register(FormDefinition, FormDefinitionAdmin)
