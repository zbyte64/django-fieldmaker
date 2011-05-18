from django import forms
from django.utils.datastructures import SortedDict

from resource import field_registry
from spec_widget import MetaForm

class FormSpecification(object):
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
            field_maker = field_registry.fields[field_def['field']]
            widget_maker = field_registry.widgets[field_def['widget']]
            
            widget = widget_maker.create_widget(field_def['widget_spec'])
            field_kwargs = field_def['field_spec']
            field = field_maker.create_field(field_kwargs, widget=widget)
            
            field_dict[field_def['name']] = field
        return field_dict
    
    def extend_form(self, form, data):
        form.fields.update(self.get_fields(data))

field_registry.register_form_specification(FormSpecification.version, FormSpecification())

