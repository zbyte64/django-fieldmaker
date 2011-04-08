from django.utils import unittest

from resource import field_registry

class FormSpecificationTestCase(unittest.TestCase):
    def test_create_form(self):
        from form_specifications import FormSpecification
        spec = FormSpecification()
        form_cls = spec.create_form(spec.example)
        self.assertEqual(len(form_cls.base_fields), len(spec.example['fields']))
        form = form_cls()
        self.assertEqual(len(form.fields), len(spec.example['fields']))
        assert 'email' in form.fields
    
    def test_get_fields(self):
        from form_specifications import FormSpecification
        spec = FormSpecification()
        fields = spec.get_fields(spec.example)
        self.assertEqual(len(fields), len(spec.example['fields']))
