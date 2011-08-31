from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe

from resource import field_registry
from utils import prep_for_kwargs
import html5widgets
import spec_widget

class BaseWidgetForm(forms.Form):
    classes = forms.CharField(required=False)
    
    def clean(self):
        for key, value in self.cleaned_data.items():
            if value in ("", None):
                del self.cleaned_data[key]
        return self.cleaned_data

class BaseWidget(object):
    form = BaseWidgetForm
    widget = None
    html5widget = None
    identities = []
    
    def create_widget(self, data):
        data = dict(data)
        if 'classes' in data:
            data.setdefault('attrs', {})
            data['attrs'].setdefault('class', data.pop('classes'))
        html5 = self.html5widget and data.pop('html5', False)
        if html5:
            return self.html5widget(**prep_for_kwargs(data))
        else:
            return self.widget(**prep_for_kwargs(data))
    
    def get_form(self):
        return self.form
    
    def render_for_admin(self, key):
        return mark_safe('<table class="%s">%s</table>' % (key, self.get_form()(prefix='prefix').as_table()))

class TextInput(BaseWidget):
    widget = widgets.TextInput
    identities = ['CharField', 'DateField', 'DateTimeField', 'DecimalField', 'EmailField', 'FloatField', 'IntegerField', 'IPAddressField', 'RegexField', 'SlugField', 'TimeField', 'URLField']

field_registry.register_widget('TextInput', TextInput)

class PasswordInputWidgetForm(BaseWidgetForm):
    render_value = forms.BooleanField(required=False, initial=True)

class PasswordInput(BaseWidget):
    widget = widgets.PasswordInput
    identities = ['CharField']

field_registry.register_widget('PasswordInput', PasswordInput)

class HiddenInput(BaseWidget):
    widget = widgets.HiddenInput

field_registry.register_widget('HiddenInput', HiddenInput)

class MultipleHiddenInput(BaseWidget):
    widget = widgets.MultipleHiddenInput

field_registry.register_widget('MultipleHiddenInput', MultipleHiddenInput)

class FileInput(BaseWidget):
    widget = widgets.FileInput
    identities = ['FileField']

field_registry.register_widget('FileInput', FileInput)

class ClearableFileInput(FileInput):
    widget = widgets.ClearableFileInput

field_registry.register_widget('ClearableFileInput', ClearableFileInput)

class Textarea(BaseWidget):
    widget = widgets.Textarea
    identities = ['CharField']

field_registry.register_widget('Textarea', Textarea)

class DateInputWidgetForm(BaseWidgetForm):
    format = forms.CharField(required=False)

class DateInput(BaseWidget):
    widget = widgets.DateInput
    html5widget = html5widgets.DateInput
    form = DateInputWidgetForm
    identities = ['DateField']

field_registry.register_widget('DateInput', DateInput)

class DateTimeInputWidgetForm(BaseWidgetForm):
    format = forms.CharField(required=False)

class DateTimeInput(BaseWidget):
    widget = widgets.DateTimeInput
    html5widget = html5widgets.DateTimeInput
    form = DateTimeInputWidgetForm
    identities = ['DateTimeField']

field_registry.register_widget('DateTimeInput', DateTimeInput)

class TimeInputWidgetForm(BaseWidgetForm):
    format = forms.CharField(required=False)

class TimeInput(BaseWidget):
    widget = widgets.TimeInput
    form = TimeInputWidgetForm
    identities = ['TimeField']

field_registry.register_widget('TimeInput', TimeInput)

class CheckboxInput(BaseWidget):
    widget = widgets.CheckboxInput
    identities = ['BooleanField']

field_registry.register_widget('CheckboxInput', CheckboxInput)

class Select(BaseWidget):
    widget = widgets.Select
    #TODO choices
    form = BaseWidgetForm
    identities = ['ChoiceField']

field_registry.register_widget('Select', Select)

class NullBooleanSelect(BaseWidget):
    widget = widgets.NullBooleanSelect
    identities = ['ChoiceField']

field_registry.register_widget('NullBooleanSelect', NullBooleanSelect)

class SelectMultiple(BaseWidget):
    widget = widgets.SelectMultiple
    identities = ['MultipleChoiceField']

field_registry.register_widget('SelectMultiple', SelectMultiple)

class RadioSelect(BaseWidget):
    widget = widgets.RadioSelect
    identities = ['ChoiceField']

field_registry.register_widget('RadioSelect', RadioSelect)

class CheckboxSelectMultiple(BaseWidget):
    widget = widgets.CheckboxSelectMultiple
    identities = ['MultipleChoiceField']

field_registry.register_widget('CheckboxSelectMultiple', CheckboxSelectMultiple)

class SlpitDateTimeInputWidgetForm(BaseWidgetForm):
    date_format = forms.CharField(required=False)
    time_format = forms.CharField(required=False)

class SplitDateTimeWidget(BaseWidget):
    widget = widgets.SplitDateTimeWidget
    form = SlpitDateTimeInputWidgetForm
    identities = ['DateTimeField']

field_registry.register_widget('SplitDateTimeWidget', SplitDateTimeWidget)

class SplitHiddenDateTimeWidget(BaseWidget):
    widgets = widgets.SplitHiddenDateTimeWidget
    form = SlpitDateTimeInputWidgetForm
    identities = ['DateTimeField']

field_registry.register_widget('SplitHiddenDateTimeWidget', SplitHiddenDateTimeWidget)

#HTML 5 WIDGETS#

'''
class DateInput(BaseWidget):
    widget = html5widgets.DateInput
    identities = []

field_registry.register_widget('DateInput', DateInput)
'''
class EmailInput(BaseWidget):
    widget = html5widgets.EmailInput
    identities = ['EmailField']

field_registry.register_widget('EmailInput', EmailInput)

class NumberInput(BaseWidget):
    widget = html5widgets.NumberInput
    identities = ['DecimalField', 'FloatField', 'IntegerField']

field_registry.register_widget('NumberInput', NumberInput)

class TelephoneInput(BaseWidget):
    widget = html5widgets.TelephoneInput
    identities = ['CharField']

field_registry.register_widget('TelephoneInput', TelephoneInput)

class URLInput(BaseWidget):
    widget = html5widgets.URLInput
    identities = ['URLField']

field_registry.register_widget('URLInput', URLInput)

class FormWidget(BaseWidget):
    widget = spec_widget.FormWidget
    identities = ['FormField']

field_registry.register_widget('FormWidget', FormWidget)

class ListFormWidget(BaseWidget):
    widget = spec_widget.ListFormWidget
    identities = ['ListFormField']

field_registry.register_widget('ListFormWidget', ListFormWidget)

