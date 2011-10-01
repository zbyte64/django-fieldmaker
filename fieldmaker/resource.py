

class Registry(object):
    default_versions = ['base.1']
    
    def __init__(self):
        self.widgets = dict()
        self.form_specifications = dict()
    
    def register_form_specification(self, name, specification):
        assert name not in self.form_specifications
        if isinstance(specification, type):
            specification = specification()
        self.form_specifications[name] = specification
    
    def register_field(self, name, field, versions=None):
        import form_specifications
        for version in versions or self.default_versions:
            self.form_specifications[version].register_field(name, field)
    
    def register_widget(self, name, widget, versions=None):
        import form_specifications
        for version in versions or self.default_versions:
            self.form_specifications[version].register_widget(name, widget)
        
        assert name not in self.widgets
        if isinstance(widget, type):
            widget = widget()
        self.widgets[name] = widget


registry = Registry()
field_registry = registry

class FieldRegistry(object): #TODO make inheritable
    def __init__(self):
        self.fields = dict()
        self.widgets = dict()
    
    def register_field(self, name, field):
        assert name not in self.fields
        if isinstance(field, type):
            field = field()
        self.fields[name] = field
    
    def register_widget(self, name, widget):
        assert name not in self.widgets
        if isinstance(widget, type):
            widget = widget()
        self.widgets[name] = widget

