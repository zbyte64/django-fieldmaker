from django import forms
from django.utils.datastructures import SortedDict

from resource import field_registry

class FormSpecification(object):
    version = 'base.1'
    example = {'form_specification':version,
               'fields': [
                   {'name':'email',
                    'field':'EmailField',
                    'field_spec':{'max_length':'128'},
                    'widget':'TextInput',
                    'widget_spec':{},}
               ]}
    
    def create_form(self, data):
        class GeneratedForm(forms.Form):
            pass
            
        GeneratedForm.base_fields = self.get_fields(data)
        return GeneratedForm
    
    def get_fields(self, data):
        field_dict = SortedDict()
        for field_def in data['fields']:
            #fetch the makers
            field_maker = field_registry.fields[field_def['field']]
            widget_maker = field_registry.widgets[field_def['widget']]
            
            widget = widget_maker.create_widget(field_def['widget_spec'])
            field_kwargs = dict(field_def['field_spec'])
            field_kwargs['widget'] = widget
            field = field_maker.create_field(field_kwargs)
            
            field_dict[field_def['name']] = field
        return field_dict
    
    def extend_form(self, form, data):
        form.fields.update(self.get_fields(data))
    
    def bound_field_form_set_to_data(self, formset):
        #CONSIDER moving this to part of the form
        data = {'form_specification':self.version,
                'fields':list(),}
        assert formset.is_valid()
        for form in formset:
            if formset.can_delete and formset._should_delete_form(form):
                continue
            form_data = form.cleaned_data
            if not form_data: continue
            field = {'name':form_data['name'],
                     'field':form_data['field'],
                     'field_spec':form_data['field_spec'],
                     'widget':form_data['widget'],
                     'widget_spec':form_data['widget_spec'],}
            data['fields'].append(field)
        return data
    
    def data_to_field_form_set_initial(self, data):
        return data.get('fields', [])

field_registry.register_form_specification(FormSpecification.version, FormSpecification())

