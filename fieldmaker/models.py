from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils import simplejson
from django.utils.functional import lazy

from resource import field_registry

class GenericObjectStore(models.Model):
    facet = models.CharField(max_length=128, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    data = models.TextField()
    
    class Meta:
        unique_together = [('facet', 'content_type', 'object_id')]

def form_spec_choices():
    choices = field_registry.form_specifications.keys()
    return zip(choices, choices)

class FormDefinition(models.Model):
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

