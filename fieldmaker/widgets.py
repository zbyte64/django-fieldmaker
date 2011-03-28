from django import forms
from django.forms import widgets

from resource import field_registry

class BaseWidgetForm(forms.Form):
    pass

class BaseWidget(object):
    form = BaseWidgetForm
    widget = None
    
    def create_widget(self, data):
        return self.widget(**data)

class TextInput(BaseWidget):
    widget = widgets.TextInput

field_registry.register_widget('TextInput', TextInput)

class PasswordInputWidgetForm(BaseWidgetForm):
    render_value = forms.BooleanField(required=False, initial=True)

class PasswordInput(BaseWidget):
    widget = widgets.PasswordInput

field_registry.register_widget('PasswordInput', PasswordInput)

class HiddenInput(BaseWidget):
    widget = widgets.HiddenInput

field_registry.register_widget('HiddenInput', HiddenInput)

class MultipleHiddenInput(BaseWidget):
    widget = widgets.MultipleHiddenInput

field_registry.register_widget('MultipleHiddenInput', MultipleHiddenInput)

class FileInput(BaseWidget):
    widget = widgets.FileInput

field_registry.register_widget('FileInput', FileInput)

class Textarea(BaseWidget):
    widget = widgets.Textarea

field_registry.register_widget('Textarea', Textarea)

class DateInputWidgetForm(BaseWidgetForm):
    format = forms.CharField(required=False)

class DateInput(BaseWidget):
    widget = widgets.DateInput
    form = DateInputWidgetForm

field_registry.register_widget('DateInput', DateInput)

class DateTimeInputWidgetForm(BaseWidgetForm):
    format = forms.CharField(required=False)

class DateTimeInput(BaseWidget):
    widget = widgets.DateTime
    form = DateTimeInputWidgetForm

field_registry.register_widget('DateTimeInput', DateTimeInput)

class TimeInputWidgetForm(BaseWidgetForm):
    format = forms.CharField(required=False)

class TimeInput(BaseWidget):
    widget = widgets.TimeInput
    form = TimeInputWidgetForm

field_registry.register_widget('TimeInput', TimeInput)

class CheckboxInput(BaseWidget):
    widget = widgets.CheckboxInput

field_registry.register_widget('CheckboxInput', CheckboxInput)

class Select(BaseWidget):
    widget = widgets.Select
    #TODO choices
    form = BaseWidgetForm

field_registry.register_widget('Select', Select)

class NullBooleanSelect(BaseWidget):
    widget = widgets.NullBooleanSelect

field_registry.register_widget('NullBooleanSelect', NullBooleanSelect)

class SelectMultiple(BaseWidget):
    widget = widgets.SelectMultiple

field_registry.register_widget('SelectMultiple', SelectMultiple)

class RadioInput(BaseWidget):
    widget = widgets.RadioInput

field_registry.register_widget('RadioInput', RadioInput)

class RadioSelect(BaseWidget):
    widget = widgets.RadioSelect

field_registry.register_widget('RadioSelect', RadioSelect)

class CheckboxSelectMultiple(BaseWidget):
    widget = widgets.CheckboxSelectMultiple

field_registry.register_widget('CheckboxSelectMultiple', CheckboxSelectMultiple)

class SlpitDateTimeInputWidgetForm(BaseWidgetForm):
    date_format = forms.CharField(required=False)
    time_format = forms.CharField(required=False)

class SplitDateTimeWidget(BaseWidget):
    widget = widgets.SplitDateTimeWidget
    form = SlpitDateTimeInputWidgetForm

field_registry.register_widget('SplitDateTimeWidget', SplitDateTimeWidget)

class SplitHiddenDateTimeWidget(BaseWidget):
    widgets = widgets.SplitHiddenDateTimeWidget
    form = SlpitDateTimeInputWidgetForm

field_registry.register_widget('SplitHiddenDateTimeWidget', SplitHiddenDateTimeWidget)

