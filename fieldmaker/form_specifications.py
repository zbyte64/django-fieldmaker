from django import forms
from django.utils.datastructures import SortedDict

from resource import registry, FieldRegistry
from spec_widget import MetaForm

class FormSpecification(object):
    def __init__(self):
        self.field_registry = FieldRegistry()
    
    version = 'base.1'
    example = [
                   {'name':'email',
                    'field':'EmailField',
                    'field_spec':{'max_length':'128'},
                    'widget':'TextInput',
                    'widget_spec':{},}
              ]
    
    def create_form(self, data):
        class GeneratedForm(MetaForm):
            pass
            
        GeneratedForm.base_fields = self.get_fields(data)
        return GeneratedForm
    
    def get_fields(self, data):
        field_dict = SortedDict()
        for field_def in data:
            #fetch the makers
            try:
                field_maker = self.field_registry.fields[field_def['field']]
            except KeyError:
                print self, self.field_registry.fields
                raise
            widget_maker = self.field_registry.widgets[field_def['widget']]
            
            widget = widget_maker.create_widget(field_def['widget_spec'])
            field_kwargs = field_def['field_spec']
            field = field_maker.create_field(field_kwargs, widget=widget)
            
            field_dict[field_def['name']] = field
        return field_dict
    
    def extend_form(self, form, data):
        form.fields.update(self.get_fields(data))
    
    def register_field(self, name, field):
        self.field_registry.register_field(name, field)
    
    def register_widget(self, name, widget):
        self.field_registry.register_widget(name, widget)
    
    @property
    def fields(self):
        return self.field_registry.fields
    
    @property
    def widgets(self):
        return self.field_registry.widgets

default_form_specification = FormSpecification()

registry.register_form_specification(FormSpecification.version, default_form_specification)

