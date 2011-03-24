class FieldRegistry(object):
    def __init__(self):
        self.fields = dict()
        self.widgets = dict()
    
    def register_field(self, field, name):
        assert name not in self.fields
        self.fields[name] = field
    
    def register_widget(self, widget, name):
        assert name not in self.widgets
        self.widgets[name] = widget

field_registry = FieldRegistry()

