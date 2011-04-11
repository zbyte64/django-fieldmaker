from django.utils import unittest
from django.test import TestCase
from django.db import models

from resource import field_registry
from form_specifications import FormSpecification
from admin.forms import FieldEntryFormSet
from forms import ExpandableModelForm
from models import FormDefinition, GenericObjectStore
from modelfields import FacetField

class TestModel(models.Model):
    attributes = FacetField()

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
        formset = FieldEntryFormSet(initial=initial)
        #print formset
        data = {'form-0-name':'email',
                'form-0-field':'EmailField',
                'form-0-field-max_length':'128',
                'form-0-widget':'TextInput',
                'form-TOTAL_FORMS':'2',
                'form-INITIAL_FORMS':'1',
                'form-MAX_NUM_FORMS':'5',}
        formset = FieldEntryFormSet(data=data)
        self.assertTrue(formset.is_valid(), str(formset.errors))
        #print formset
        data = spec.bound_field_form_set_to_data(formset)
        
        #test loading this data
        fields = spec.get_fields(spec.example)
        self.assertEqual(len(fields), 1)

class ExpandableModelFormTestCase(TestCase):
    fixtures = ['test_fieldmaker']
    
    def setUp(self):
        class ExpandableFormDefinitionForm(ExpandableModelForm):
            class Meta:
                model = FormDefinition
                form_key = 'test'
        self.form_cls = ExpandableFormDefinitionForm
    
    def test_expandable_form(self):
        form = self.form_cls()
        self.assertTrue('Field1' in form.fields)
        
        instance = FormDefinition.objects.all()[0]
        form = self.form_cls(instance=instance)
        data = form.initial
        data['Field1'] = 'foo'
        form = self.form_cls(instance=instance, data=data)
        self.assertTrue(form.is_valid(), str(form.errors))
        form.save()
        
        facet_data = GenericObjectStore.objects.lookup_facet(instance, '')
        self.assertTrue('Field1' in facet_data)

class TestFacetField(unittest.TestCase):
    def setUp(self):
        self.object = TestModel()
        self.object.save()
    
    def test_face_field(self):
        self.assertEqual(len(self.object.attributes), 0)
        self.object.attributes['foo'] = 'bar'
        self.object.attributes['bar'] = 'bacon'
        self.object.attributes.save()
        
        self.object = TestModel.objects.get(pk=self.object.pk)
        self.assertEqual(len(self.object.attributes), 2)

