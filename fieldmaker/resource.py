class FieldRegistry(object):
    def __init__(self):
        self.fields = dict()
        self.widgets = dict()
        self.form_specifications = dict()
    
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
    
    def register_form_specification(self, name, specification):
        assert name not in self.form_specifications
        if isinstance(specification, type):
            specification = specification()
        self.form_specifications[name] = specification

field_registry = FieldRegistry()

