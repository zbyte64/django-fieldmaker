from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from resource import field_registry

class GenericObjectStore(models.Model):
    facet = models.CharField(max_length=128, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    data = models.TextField()
    
    class Meta:
        unique_together = [('facet', 'content_type', 'object_id')]

class FormDefinition(models.Model):
    name = models.CharField(max_length=128)
    form_specification = models.CharField(max_length=128)
    
    data = models.TextField()
    
    def __unicode__(self):
        return self.name
    
    def get_data(self):
        from django.utils import simplejson
        return simplejson.dumps(self.data)
    
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

