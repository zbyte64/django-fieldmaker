from django.forms import widgets
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

class FormWidget(widgets.Widget):
    
    def __init__(self, *args, **kwargs):
        self.form = kwargs.pop('form', None)
        super(FormWidget, self).__init__(*args, **kwargs)

    def render(self, name, node, attrs=None):
        '''
        Expects json
        '''
        if not attrs:
            attrs = {}
        final_attrs = self.build_attrs(attrs)
        if self.form:
            return mark_safe(u'<table%s>%s</table>' % (flatatt(final_attrs), self.form.as_table()))
        return mark_safe(u'<table%s>&nbsp;</table>' % flatatt(final_attrs))
    
    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.
        """
        our_data = dict()
        #TODO multi values and file support
        for key, value in data.iteritems():
            if key.startswith(name):
                our_data[key] = value
        return our_data
    
    def _has_changed(self, initial_value, data_value):
        if not initial_value and not data_value:
            return False
        return super(FormWidget, self)._has_changed(initial_value, data_value)

