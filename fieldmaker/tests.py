from django.utils import unittest

from resource import field_registry
from form_specifications import FormSpecification
from forms import FieldEntryFormSet

class FormSpecificationTestCase(unittest.TestCase):
    def test_create_form(self):
        spec = FormSpecification()
        form_cls = spec.create_form(spec.example)
        self.assertEqual(len(form_cls.base_fields), len(spec.example['fields']))
        form = form_cls()
        self.assertEqual(len(form.fields), len(spec.example['fields']))
        assert 'email' in form.fields
    
    def test_get_fields(self):
        spec = FormSpecification()
        fields = spec.get_fields(spec.example)
        self.assertEqual(len(fields), len(spec.example['fields']))
    
    def test_form_field_integration(self):
        spec = FormSpecification()
        initial = spec.data_to_field_form_set_initial(spec.example)
        formset = FieldEntryFormSet(initial=initial)#, data=initial)
        #self.assertTrue(formset.is_valid(), str(formset.errors))
        #print formset
