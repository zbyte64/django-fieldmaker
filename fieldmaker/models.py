from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils import simplejson
from django.utils.functional import lazy

from resource import field_registry

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
        stored_obj.set_data(data)
        stored_obj.save()
        return stored_obj

class GenericObjectStore(models.Model):
    facet = models.CharField(max_length=128, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    data = models.TextField()
    
    objects = GenericObjectStoreManager()
    
    def get_data(self):
        if not self.data:
            return {}
        return simplejson.loads(self.data)
    
    def set_data(self, data):
        self.data = simplejson.dumps(data)
    
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
            return {}
        return simplejson.loads(self.data)
    
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

