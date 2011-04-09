from django import forms

from models import FormDefinition, GenericObjectStore

class ExpandableModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GenericAttributeModelForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            fields = self.get_expanded_fields()
            data = self.get_expanded_data(self.instance)
            self.fields.update(fields)
            self.initial.update(data)
    
    def get_expanded_fields(self):
        form_key = getattr(self.Meta, 'form_key', '')
        try:
            form_definition = FormDefinition.objects.get(key=form_key)
        except FormDefinition.DoesNotExist:
            return dict()
        return form_defininition.get_fields()
    
    def get_expanded_data(self, instance):
        facet = getattr(self.Meta, 'facet', '')
        return GenericObjectStore.objects.lookup_facet(instance, facet)
    
    def get_expanded_clean_data(self):
        cleaned_data = dict()
        for key in self.get_expanded_fields().iterkeys():
            if key in self.cleaned_data:
                cleaned_data[key] = self.cleaned_data[key]
        return cleaned_data
    
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

