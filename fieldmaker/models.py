from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

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
