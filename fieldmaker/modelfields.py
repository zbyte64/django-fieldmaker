from models import GenericObjectStore

class Facet(dict):
    def __init__(self, instance, facet_name, *args, **kwargs):
        super(Facet, self).__init__(*args, **kwargs)
        self.instance = instance
        self.facet_name = facet_name
        if instance.pk:
            self.load()
    
    def save(self):
        GenericObjectStore.objects.store_facet(self.instance, self.facet_name, self)
    
    def load(self):
        self.update(GenericObjectStore.objects.lookup_facet(self.instance, self.facet_name))

class FacetField(object):
    """
    class MyModel(models.Model):
        attributes = FacetField()
    
    mymodel = MyModel.objects.get(pk=1)
    mymodel.attributes['foo'] = 'bar'
    mymodel.attributes.save()
    
    """

    def __init__(self, facet=''):
        self.facet = facet

    def contribute_to_class(self, cls, name):
        self.name = name
        cls._meta.add_virtual_field(self)

        # Connect myself as the descriptor for this field
        setattr(cls, name, self)

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return None
        cache_attr = '__%s_cache' % self.name
        if not hasattr(instance, cache_attr):
            setattr(instance, cache_attr, Facet(instance, self.facet))
        return getattr(instance, cache_attr)

    def get_db_prep_lookup(self, *args, **kwargs):
        raise NotImplemented
