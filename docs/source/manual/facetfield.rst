Using FacetField
================

``FacetField`` is used to associate generic data to an instance. A model may have more then one FacetField provided they each are passed a different facet key. If you use an ExpandableModelAdmin or an ExpandableModelForm then one can add a FacetField to allow for easy access of that data.

Example usage::

    from django.db import models
    from django.core.files import File
    from fieldmaker.modelfields import FacetField
    
    class MyModel(models.Model):
        attributes = FacetField()
    
    
    mymodel = MyModel.objects.get(pk=1)
    mymodel.attributes['foo'] = 'bar'
    mymodel.attributes['somefile'] = File(open('/path/to/file.txt', 'r'))
    mymodel.attributes.save()

