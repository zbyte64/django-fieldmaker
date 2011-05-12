from django.forms import widgets
from django import forms
from django.forms.formsets import formset_factory
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

class FormWidget(widgets.Widget):
    def __init__(self, *args, **kwargs):
        form = kwargs.pop('form', None)
        if form:
            self.set_form(form)
        super(FormWidget, self).__init__(*args, **kwargs)
    
    def set_form(self, form):
        self.form = form

    def render(self, name, node, attrs=None):
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

class FormField(forms.Field):
    widget = FormWidget
    
    def __init__(self, *args, **kwargs):
        self.form_cls = kwargs.pop('form')
        self.field_form = None
        super(FormField, self).__init__(*args, **kwargs)
    
    def post_form_init(self, name, form):
        #this must be called in order for this field to work properly
        self.field_form = self.create_field_form(name, form)
        self.widget.set_form(self.field_form)
    
    def create_field_form(self, name, form):
        prefix = form.add_prefix(name)
        return self.form_cls(data=form.data or None, prefix=prefix, initial=form.initial.get(name))
    
    def clean(self, value):
        value = super(FormField, self).clean(value)
        if self.field_form:
            if not self.field_form.is_valid():
                raise forms.ValidationError('Please correct the errors below')
            return self.field_form.cleaned_data
        return value

class ListFormWidget(FormWidget):
    pass
    #TODO provide media to allow for dynamic adding

class ListFormField(FormField):
    widget = ListFormWidget
    
    def create_field_form(self, name, form):
        prefix = form.add_prefix(name)
        formset = formset_factory(self.form_cls) #TODO allow for configuration
        return formset(data=form.data or None, prefix=prefix, initial=form.initial.get(name))

def post_form_init(form):
    for name, field in form.fields.iteritems():
        if hasattr(field, 'post_form_init'):
            field.post_form_init(name, form)

