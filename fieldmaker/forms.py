from django import forms
from django.forms.formsets import formset_factory

from resource import field_registry

class FieldEntryForm(forms.Form):
    name = forms.CharField()
    field = forms.ChoiceField(choices=[])
    widget = forms.ChoiceField(choices=[])
    
    def __init__(self, *args, **kwargs):
        super(FieldEntryForm, self).__init__(*args, **kwargs)
        self.load_field_form()
        self.load_widget_form()
    
    def populate_field_choices(self):
        self['field'].choices = field_registry.fields.items()
    
    def populate_widget_choices(self):
        self['widget'].choices = field_registry.widgets.items()
    
    def get_active_field_value(self, field_name):
        if hasattr(self, 'cleaned_data'):
            return self.cleaned_data[field_name]
        key = field_name
        if self.prefix:
            key = '%s-%s' % (self.prefix, key)
        if self.data and key in self.data:
            return self.data.get(key)
        if self.initial:
            return self.initial.get(field_name)
        return None
    
    def create_field_form(self):
        field = self.get_active_field_value('field')
        if field is None: return
        field = field()
        form_cls = field.get_form()
        if self.prefix:
            prefix = '%s-field' % self.prefix
        else:
            prefix = 'field'
        
        self.fields['widget'].choices = field.widget_choices()
        self.fields['widget'].initial = field.default_widget
        
        return form_cls(data=self.data, prefix=prefix)
    
    def create_widget_form(self):
        field = self.get_active_field_value('widget')
        if field is None: return
        field = field()
        form_cls = field.get_form()
        if self.prefix:
            prefix = '%s-widget' % self.prefix
        else:
            prefix = 'widget'
        return form_cls(data=self.data, prefix=prefix)
    
    def load_field_form(self):
        self.field_form = self.create_field_form()
    
    def load_widget_form(self):
        self.widget_form = self.create_widget_form()
    
    def clean(self):
        self.load_field_form()
        self.load_widget_form()
        if self.field_form:
            self.field_form.is_valid()
        if self.widget_form:
            self.widget_form.is_valid()
        return self.cleaned_data

FieldEntryFormSet = formset_factory(FieldEntryForm)

