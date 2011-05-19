from django.forms import widgets
from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
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
        if self.form:
            return self.form.has_changed()
        if not initial_value and not data_value:
            return False
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
    def _media(self):
        from django.conf import settings
        js = ['js/jquery.min.js', 'js/jquery.init.js', 'js/inlines.min.js']
        return forms.Media(js=['%s%s' % (settings.ADMIN_MEDIA_PREFIX, url) for url in js])
    media = property(_media)
    
    def render(self, name, node, attrs=None):
        if not attrs:
            attrs = {}
        final_attrs = self.build_attrs(attrs)
        if self.form: #TODO move this to BaseListFormSet
            parts = list()
            for form in self.form.forms:
                parts.append(u'<tr><td><table class="module">%s</table></td></tr>' % form.as_table())
            parts.append(u'<tr id="%s-empty" class="empty-form"><td><table class="module">%s</table></td></tr>' % (self.form.prefix, self.form.empty_form.as_table()))
            return mark_safe(u'%s<table%s> %s</table>' % (self.form.management_form.as_table(), flatatt(final_attrs), u'\n'.join(parts)))
        return mark_safe(u'<table%s>&nbsp;</table>' % flatatt(final_attrs))

class BaseListFormSet(BaseFormSet):
    def _get_cleaned_data(self):
        """
        Returns a list of form.cleaned_data dicts for every form in self.forms.
        """
        if not self.is_valid():
            raise AttributeError("'%s' object has no attribute 'cleaned_data'" % self.__class__.__name__)
        result = list()
        for form in self.forms:
            form.full_clean()
            if self.can_delete:
                if self._should_delete_form(form):
                    continue
                elif form.is_valid():
                    data = dict(form.cleaned_data)
                    data.pop('DELETE', None)
                    if data or form.has_changed():
                        result.append(data)
            elif form.is_valid():
                if form.cleaned_data or form.has_changed():
                    result.append(form.cleaned_data)
        return result
    cleaned_data = property(_get_cleaned_data)
    
    def is_valid(self):
        """
        Returns True if form.errors is empty for every form in self.forms.
        """
        if not self.is_bound:
            return False
        # We loop over every form.errors here rather than short circuiting on the
        # first failure to make sure validation gets triggered for every form.
        forms_valid = True
        err = self.errors
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            if self.can_delete:
                if self._should_delete_form(form):
                    # This form is going to be deleted so any of its errors
                    # should not cause the entire formset to be invalid.
                    continue
            if bool(self.errors[i]) and bool(form.changed_data):
                forms_valid = False
        return forms_valid and not bool(self.non_form_errors())
    
    def _get_changed_data(self):
        if getattr(self, '_changed_data', None) is None:
            self._changed_data = []
            for i in range(0, self.total_form_count()):
                form = self.forms[i]
                self._changed_data.append(form.changed_data)
        return self._changed_data
    changed_data = property(_get_changed_data)
    
    def has_changed(self):
        for entry in self.changed_data:
            if len(entry): return True
        return False

class ListFormField(FormField):
    widget = ListFormWidget
    can_delete = True
    formset = BaseListFormSet
    
    def create_field_form(self, name, form):
        prefix = form.add_prefix(name)
        formset = formset_factory(self.form_cls,
                                  formset=self.formset,
                                  can_delete=self.can_delete) #TODO allow for configuration
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

