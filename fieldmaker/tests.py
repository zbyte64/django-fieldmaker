from django.utils import unittest
from django.test import TestCase
from django import forms
from django.db import models
from django.core.files.base import ContentFile

from resource import field_registry
from form_specifications import default_form_specification
from forms import ExpandableModelForm
from models import FormDefinition, GenericObjectStore
from modelfields import FacetField
from spec_widget import FormField, ListFormField, MetaForm

class TestModel(models.Model):
    attributes = FacetField()

class FormSpecificationTestCase(unittest.TestCase):
    def test_create_form(self):
        spec = default_form_specification
        form_cls = spec.create_form(spec.example)
        self.assertEqual(len(form_cls.base_fields), len(spec.example))
        form = form_cls()
        self.assertEqual(len(form.fields), len(spec.example))
        assert 'email' in form.fields
    
    def test_get_fields(self):
        spec = default_form_specification
        fields = spec.get_fields(spec.example)
        self.assertEqual(len(fields), len(spec.example))

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
    
    def test_facet_field(self):
        self.assertEqual(len(self.object.attributes), 0)
        self.object.attributes['foo'] = 'bar'
        self.object.attributes['bar'] = 'bacon'
        self.object.attributes.save()
        
        self.object = TestModel.objects.get(pk=self.object.pk)
        self.assertEqual(len(self.object.attributes), 2)
    
    def test_facet_field_file_store(self):
        cf = ContentFile('foo')
        self.object.attributes['myfile'] = cf
        self.object.attributes.save()
        
        self.object = TestModel.objects.get(pk=self.object.pk)
        myfile = self.object.attributes['myfile']
        self.assertEqual(myfile.read(), 'foo')
        
        self.object.attributes.save()
        
        cf = ContentFile('bar')
        self.object.attributes['myfile'] = cf
        self.object.attributes.save()
        self.object.attributes.load()
        self.assertEqual(self.object.attributes['myfile'].read(), 'bar')

class TestMetaFields(unittest.TestCase):
    def test_form_field(self):
        class PersonForm(forms.Form):
            first_name = forms.CharField()
            last_name = forms.CharField()
        
        class PeopleForm(MetaForm):
            person_one = FormField(form=PersonForm)
            person_two = FormField(form=PersonForm)
        
        form = PeopleForm()
        form_html = unicode(form)
        self.assertTrue('id_person_one-last_name' in form_html)
        
        form = PeopleForm(data={})
        self.assertFalse(form.is_valid())
        
        initial = {'person_one': {'first_name':'John', 'last_name':'Smith'},
                   'person_two': {'first_name':'Jane', 'last_name':'Doe'},}
        form = PeopleForm(initial=initial)
        form_html = unicode(form)
        self.assertTrue('value="John"' in form_html)
        
        data = {'person_one-first_name':'John',
                'person_one-last_name':'Smith',
                'person_two-first_name':'Jane',
                'person_two-last_name':'Doe',}
        form = PeopleForm(initial=initial, data=data)
        self.assertTrue(form.is_valid())
        form_html = unicode(form)
        self.assertTrue('value="John"' in form_html)
        self.assertEqual(initial, form.cleaned_data)
    
    def test_double_nested_form(self):
        pass
    
    def test_list_form_field(self):
        class PersonForm(forms.Form):
            first_name = forms.CharField()
            last_name = forms.CharField()
        
        class GroupForm(MetaForm):
            group_name = forms.CharField()
            people = ListFormField(form=PersonForm)
        
        form = GroupForm()
        form_html = unicode(form)
        self.assertTrue('id_people-0-first_name' in form_html)
        
        form = GroupForm(data={})
        self.assertFalse(form.is_valid())
        
        initial = {'group_name': 'anonymous',
                   'people': [{'first_name':'John', 'last_name':'Smith'},
                              {'first_name':'Jane', 'last_name':'Doe'},],}
        form = GroupForm(initial=initial)
        form_html = unicode(form)
        self.assertTrue('value="John"' in form_html)
        
        data = {'group_name': 'anonymous',
                'people-TOTAL_FORMS': '3',
                'people-INITIAL_FORMS': '2',
                'people-0-first_name':'John',
                'people-0-last_name':'Smith',
                'people-1-first_name':'Jeniffer',
                'people-1-last_name':'Dane',
                'people-2-first_name':'',
                'people-2-last_name':'',}
        form = GroupForm(initial=initial, data=data)
        self.assertTrue(form.is_valid())
        self.assertTrue('people' in form.changed_data)
        form_html = unicode(form)
        self.assertTrue('value="John"' in form_html)
        #print form_html
        #self.assertEqual(len(form.cleaned_data['people']), 2) #TODO don't return empty results
        
        data = {'group_name': 'anonymous',
                'people-TOTAL_FORMS': '3',
                'people-INITIAL_FORMS': '2',
                'people-0-first_name':'John',
                'people-0-last_name':'Smith',
                'people-1-first_name':'Jane',
                'people-1-last_name':'Doe',
                'people-2-first_name':'',
                'people-2-last_name':'',}
        form = GroupForm(initial=initial, data=data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.changed_data)


