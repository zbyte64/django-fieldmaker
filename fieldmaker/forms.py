from django import forms

from models import FormDefinition, GenericObjectStore
from spec_widget import MetaFormMixin

class ExpandableFormMixin(MetaFormMixin):
    def install_expanded_fields(self):
        fields = self.get_expanded_fields()
        self.fields.update(fields)
        
    def get_expanded_fields(self):
        try:
            form_definition = FormDefinition.objects.get(key=self.expanded_form_key)
        except FormDefinition.DoesNotExist:
            return dict()
        return form_definition.get_fields()
    
    def get_expanded_clean_data(self):
        cleaned_data = dict()
        for key in self.get_expanded_fields().iterkeys():
            cleaned_data[key] = self.cleaned_data.get(key, None)
        return cleaned_data
    
class ExpandableForm(forms.Form, ExpandableFormMixin):
    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        self.install_expanded_fields()
        self.post_form_init()
    
    @property
    def expanded_form_key(self):
        return getattr(self.Meta, 'form_key')

class ExpandableModelForm(forms.ModelForm, ExpandableFormMixin):
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.install_expanded_fields()
        if self.instance and self.instance.pk:
            data = self.get_expanded_data(self.instance)
            self.initial.update(data)
        self.post_form_init()
    
    @property
    def expanded_form_key(self):
        opts = self.Meta.model._meta
        return getattr(self.Meta, 'form_key', '%s_%s' % (opts.app_label, opts.module_name))
    
    def get_expanded_data(self, instance):
        facet = getattr(self.Meta, 'facet', '')
        return GenericObjectStore.objects.lookup_facet(instance, facet)
    
    def save_expanded_data(self, instance):
        data = self.get_expanded_clean_data()
        facet = getattr(self.Meta, 'facet', '')
        return GenericObjectStore.objects.store_facet(instance, facet, data)
    
    def save(self, commit=True):
        instance = super(ExpandableModelForm, self).save(commit)
        if commit:
            self.save_expanded_data(instance)
        return instance
    
    def _set_save_m2m(self, value):
        self._save_m2m = value
    
    def _get_save_m2m(self):
        def save_m2m():
            if hasattr(self, '_save_m2m'):
                self._save_m2m()
            self.save_expanded_data(self.instance)
        return save_m2m
    
    save_m2m = property(_get_save_m2m, _set_save_m2m)

