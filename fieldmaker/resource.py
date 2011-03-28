class FieldRegistry(object):
    def __init__(self):
        self.fields = dict()
        self.widgets = dict()
    
    def register_field(self, name, field):
        assert name not in self.fields
        self.fields[name] = field
    
    def register_widget(self, name, widget):
        assert name not in self.widgets
        self.widgets[name] = widget

field_registry = FieldRegistry()

