from django import forms
from django.utils import simplejson

from resource import field_registry
from models import FormDefinition

class FormDefinitionForm(forms.ModelForm):
    form_specification = forms.CharField(widget=forms.HiddenInput)
    
    def clean_form_specification(self):
        name = self.cleaned_data.get('form_specification')
        if name:
            try:
                self.form_specification = field_registry.form_specifications[name]
            except KeyError:
                raise forms.ValidationError('Unknown form specification')
        return name
    
    def clean(self):
        data = self.cleaned_data.get('data')
        if data:
            try:
                json_data = simplejson.loads(data)
            except ValueError, error:
                raise forms.ValidationError(unicode(error))
            else:
                try:
                    form = self.form_specification.create_form(json_data)
                except KeyError, error:
                    raise forms.ValidationError(unicode(error))
        return self.cleaned_data
    
    class Meta:
        model = FormDefinition

