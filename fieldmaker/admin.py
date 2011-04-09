from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.forms.formsets import formset_factory
from django.template.response import TemplateResponse
from django.utils.functional import update_wrapper

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
    template = 'admin/fieldmaker/formdefinition/fieldentry_stacked.html'
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
    
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        
        url_patterns = patterns('',
            url(r'^(?P<object_id>[\d\w]+)/preview/$', wrap(self.preview_form), name='fieldmaker_formdefinition_preview'),
        )
        url_patterns += super(FormDefinitionAdmin, self).get_urls()
        return url_patterns
    
    def preview_form(self, request, object_id):
        instance = self.model.objects.get(pk=object_id)
        form_cls = instance.get_form()
        if request.POST:
            form = form_cls(request.POST)
            form.is_valid()
        else:
            form = form_cls()
        return TemplateResponse(request, 'admin/fieldmaker/formdefinition/preview_form.html',
                                {'instance':instance, 'form':form,},)

admin.site.register(FormDefinition, FormDefinitionAdmin)

