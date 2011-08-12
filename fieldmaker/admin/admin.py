import copy

from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.functional import update_wrapper

from fieldmaker.models import FormDefinition, GenericObjectStore
from forms import ExpandableAdminModelForm, AdminFormDefinitionForm

def get_fieldsets(form, declared_fieldsets, expandable_fieldset, read_only_fields):
    if declared_fieldsets:
        fields = copy.deepcopy(declared_fieldsets)
        for section, dictionary in fields:
            if section != expandable_fieldset:
                continue
            if 'fields' in dictionary:
                expanded_fields = form.get_expanded_fields().keys()
                dictionary['fields'] = section_fields = list(dictionary['fields'])
                for field in expanded_fields:
                    if field not in section_fields:
                        section_fields.append(field)
                break
        return fields
    fields = form.fields.keys() + list(read_only_fields)
    return [(None, {'fields': fields})]

class ExpandableModelAdminMixin(object):
    form = ExpandableAdminModelForm
    expandable_fieldset = None
    
    def get_fieldsets(self, request, obj=None):
        "Hook for specifying fieldsets for the add form."
        form_cls = self.get_form(request, obj)
        form = form_cls(instance=obj)
        return get_fieldsets(form, self.declared_fieldsets, self.expandable_fieldset, self.get_readonly_fields(request, obj))

class ExpandableInlineAdminMixin(object):
    form = ExpandableAdminModelForm
    expandable_fieldset = None
    
    def get_fieldsets(self, request, obj=None):
        "Hook for specifying fieldsets for the add form."
        class form_cls(self.form):
            class Meta:
                model = self.model
        form = form_cls(instance=obj)
        
        return get_fieldsets(form, self.declared_fieldsets, self.expandable_fieldset, self.get_readonly_fields(request, obj))

class ExpandableModelAdmin(ExpandableModelAdminMixin, admin.ModelAdmin):
    pass

class FormDefinitionAdmin(ExpandableModelAdmin):
    form = AdminFormDefinitionForm
    
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
            if form.is_valid():
                form = form_cls(initial=form.cleaned_data)
        else:
            form = form_cls()
        return TemplateResponse(request, 'admin/fieldmaker/formdefinition/preview_form.html',
                                {'instance':instance, 'form':form,},)

admin.site.register(FormDefinition, FormDefinitionAdmin)

