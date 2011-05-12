from django.forms import widgets
from django import forms
from django.forms.formsets import formset_factory
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

def compare_dict(data1, data2):
    if set(data1.iterkeys()) != set(data2.iterkeys()):
        return False
    for key, value1 in data1.iteritems():
        value2 = data2.get(key)
        if isinstance(value1, list):
            if not compare_list(value1, value2):
                return False
        elif isinstance(value1, dict):
            if not compare_dict(value1, value2):
                return False
        elif value1 != value2:
            return False
    return True

def compare_list(data1, data2):
    if len(data1) != len(data2):
        return False
    for value1, value2 in zip(data1, data2):
        if isinstance(value1, list):
            if not compare_list(value1, value2):
                return False
        elif isinstance(value1, dict):
            if not compare_dict(value1, value2):
                return False
        elif value1 != value2:
            return False
    return True

class FormWidget(widgets.Widget):
    def __init__(self, *args, **kwargs):
        form = kwargs.pop('form', None)
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
        if self.form:
            cleaned_data = self.form.cleaned_data
            if isinstance(cleaned_data, list):
                data_value = list()
                for entry in cleaned_data:
                    if entry:
                        data_value.append(entry)
            else:
                data_value = cleaned_data
        if isinstance(data_value, dict):
            return not compare_dict(initial_value, data_value)
        if isinstance(data_value, list):
            return not compare_list(initial_value, data_value)
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
    def render(self, name, node, attrs=None):
        if not attrs:
            attrs = {}
        final_attrs = self.build_attrs(attrs)
        if self.form:
            parts = list()
            for form in self.form.forms:
                parts.append(u'<tr><td><table class="module">%s</table></td></tr>' % form.as_table())
            return mark_safe(u'%s<table%s> %s</table>' % (self.form.management_form.as_table(), flatatt(final_attrs), u'\n'.join(parts)))
        return mark_safe(u'<table%s>&nbsp;</table>' % flatatt(final_attrs))

class ListFormField(FormField):
    widget = ListFormWidget
    
    def create_field_form(self, name, form):
        prefix = form.add_prefix(name)
        formset = formset_factory(self.form_cls) #TODO allow for configuration
        return formset(data=form.data or None, prefix=prefix, initial=form.initial.get(name))
    
    def clean(self, value):
        value = super(ListFormField, self).clean(value)
        if isinstance(value, list):
            new_list = list()
            for entry in value:
                if entry:
                    new_list.append(entry)
            return new_list
        return value

class MetaFormMixin(object):
    def post_form_init(self):
        for name, field in self.fields.iteritems():
            if hasattr(field, 'post_form_init'):
                field.post_form_init(name, self)

class MetaForm(forms.Form, MetaFormMixin):
    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        self.post_form_init()

