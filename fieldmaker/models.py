import uuid

from django.db import models
from django.core.files.base import File
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils import simplejson
from django.utils.functional import lazy

from resource import field_registry

def generate_uuid():
    return uuid.uuid4().hex

class GenericFileStore(models.Model):
    key = models.CharField(max_length=128, unique=True, default=generate_uuid)
    name = models.CharField(max_length=255)
    stored_file = models.FileField(upload_to='fieldmaker/filestore/')

class GenericObjectStoreManager(models.Manager):
    def filter_for_instance(self, instance):
        ct = ContentType.objects.get_for_model(instance)
        return self.filter(content_type=ct, object_id=instance.pk)
    
    def lookup_facet(self, instance, facet):
        try:
            stored_obj = self.filter_for_instance(instance).get(facet=facet)
        except self.model.DoesNotExist:
            return {}
        else:
            return stored_obj.get_data()
    
    def store_facet(self, instance, facet, data):
        try:
            stored_obj = self.filter_for_instance(instance).get(facet=facet)
        except self.model.DoesNotExist:
            stored_obj = self.model(content_object=instance, facet=facet)
            stored_obj.save()
        stored_obj.set_data(data)
        stored_obj.save()
        return stored_obj

class GenericObjectStore(models.Model):
    facet = models.CharField(max_length=128, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    data = models.TextField()
    
    file_store = models.ManyToManyField(GenericFileStore, blank=True)
    
    objects = GenericObjectStoreManager()
    
    def get_data(self):
        if not self.data:
            return {}
        data = simplejson.loads(self.data)
        
        def handle_list(alist):
            for value in alist:
                #TODO list of files?
                if isinstance(value, dict):
                    handle_dict(value)
                elif isinstance(value, list):
                    handle_list(value)
        
        def handle_dict(dictionary):
            for key, value in dictionary.items():
                if isinstance(value, basestring):
                    if value.startswith('file://'):
                        file_key = value[len('file://'):]
                        dictionary[key] = self.file_store.get(key=file_key).stored_file
                        dictionary[key].file_key = file_key
                elif isinstance(value, list):
                    handle_list(value)
                elif isinstance(value, dict):
                    handle_dict(value)
        
        handle_dict(data)
        return data
    
    def set_data(self, data):
        seen_files = set()
        
        def handle_list(alist):
            for value in alist:
                #TODO list of files?
                if isinstance(value, dict):
                    handle_dict(value)
                elif isinstance(value, list):
                    handle_list(value)
            return alist
        
        def handle_dict(dictionary):
            dictionary = dict(dictionary)
            for key, value in dictionary.items():
                if isinstance(value, File):
                    if hasattr(value, 'file_key'):
                        dictionary[key] = 'file://%s' % value.file_key
                        seen_files.add(value.file_key)
                    else:
                        file_store = GenericFileStore()
                        file_store.name = getattr(value, 'name', None) or file_store.key
                        file_store.stored_file.save(file_store.name, value)
                        self.file_store.add(file_store)
                        dictionary[key] = 'file://%s' % file_store.key
                        seen_files.add(file_store.key)
                elif isinstance(value, list):
                    dictionary[key] = handle_list(value)
                elif isinstance(value, dict):
                    dictionary[key] = handle_dict(value)
            return dictionary
        #TODO cleanup dangling files from previous saves
        #stale_files = self.file_store.exclude(key__in=seen_files)
        data = handle_dict(data)
        self.data = simplejson.dumps(data)
    
    def get_facet_definition(self):
        try:
            return FacetDefinition.objects.get(content_type=self.content_type, facet=self.facet)
        except FacetDefinition.DoesNotExist:
            return None
    
    class Meta:
        unique_together = [('facet', 'content_type', 'object_id')]

def form_spec_choices():
    choices = field_registry.form_specifications.keys()
    return zip(choices, choices)


class FormDefinition(models.Model):
    key = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    form_specification = models.CharField(max_length=128, choices=lazy(form_spec_choices, list)())
    
    data = models.TextField()
    
    def __unicode__(self):
        return self.name
    
    def get_data(self):
        if not self.data:
            return []
        data = simplejson.loads(self.data)
        if isinstance(data, dict) and 'fields' in data:
            data = data['fields']
        if isinstance(data, list):
            new_data = list()
            for entry in data:
                if entry:
                    new_data.append(entry)
            data = new_data
        return data
    
    def set_data(self, data):
        self.data = simplejson.dumps(data)
    
    def get_form_specification(self):
        return field_registry.form_specifications[self.form_specification]
    
    def get_form(self):
        form_spec = self.get_form_specification()
        data = self.get_data()
        return form_spec.create_form(data)
    
    def get_fields(self):
        form_spec = self.get_form_specification()
        data = self.get_data()
        return form_spec.get_fields(data)

class FacetDefinition(models.Model):
    form_defintion = models.ForeignKey(FormDefinition)
    facet = models.CharField(max_length=128, blank=True)
    content_type = models.ForeignKey(ContentType)
    
    class Meta:
        unique_together = ['facet', 'content_type']

