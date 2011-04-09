from django import forms
from django.forms import widgets

from resource import field_registry

class BaseWidgetForm(forms.Form):
    classes = forms.CharField(required=False)
    
    def clean(self):
        for key, value in self.cleaned_data.items():
            if value == "":
                del self.cleaned_data[key]
        return self.cleaned_data

class BaseWidget(object):
    form = BaseWidgetForm
    widget = None
    identities = []
    
    def create_widget(self, data):
        data = dict(data)
        data.setdefault('attrs', {})
        if 'classes' in data:
            data['attrs'].setdefault('class', data.pop('classes'))
        return self.widget(**data)
    
    def get_form(self):
        return self.form

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

class Textarea(BaseWidget):
    widget = widgets.Textarea
    identities = ['CharField']

field_registry.register_widget('Textarea', Textarea)

class DateInputWidgetForm(BaseWidgetForm):
    format = forms.CharField(required=False)

class DateInput(BaseWidget):
    widget = widgets.DateInput
    form = DateInputWidgetForm
    identities = ['DateField']

field_registry.register_widget('DateInput', DateInput)

class DateTimeInputWidgetForm(BaseWidgetForm):
    format = forms.CharField(required=False)

class DateTimeInput(BaseWidget):
    widget = widgets.DateTimeInput
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

