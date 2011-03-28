from djanfo import forms
from django.forms import widgets

class BaseWidgetForm(forms.Form):
    pass

class BaseWidget(object):
    pass

class TextInputWidget(BaseWidget):
    widget = widgets.TextInput
    form = BaseWidgetForm

class PasswordInputWidget(BaseWidget):
    widget = widgets.PasswordInput
    form = BaseWidgetForm

class HiddenInputWidget(BaseWidget):
    widget = widgets.HiddenInput
    form = BaseWidgetForm

class MultipleHiddenInputWidget(BaseWidget):
    widget = widgets.MultipleHiddenInput
    form = BaseWidgetForm

class FileInputWidget(BaseWidget):
    widget = widgets.FileInput
    form = BaseWidgetForm

class TextareaWidget(BaseWidget):
    widget = widgets.Textarea
    form = BaseWidgetForm

class DateInputWidget(BaseWidget):
    widget = widgets.DateInput
    form = BaseWidgetForm

class DateTimeInputWidget(BaseWidget):
    widget = widgets.DateTime
    form = BaseWidgetForm

class TimeInputWidget(BaseWidget):
    widget = widgets.TimeInput
    form = BaseWidgetForm

class CheckboxInputWidget(BaseWidget):
    widget = widgets.CheckboxInput
    form = BaseWidgetForm

class SelectWidget(BaseWidget):
    widget = widgets.Select
    form = BaseWidgetForm

class NullBooleanSelect(BaseWidget):
    widget = widgets.NullBooleanSelect
    form = BaseWidgetForm

class SelectMultipleWidget(BaseWidget):
    widget = widgets.SelectMultiple
    form = BaseWidgetForm

class RadioInputWidget(BaseWidget):
    widget = widgets.RadioInput
    form = BaseWidgetForm

class RadioSelectWidget(BaseWidget):
    widget = widgets.RadioSelect
    form = BaseWidgetForm

class CheckboxSelectMultipleWidget(BaseWidget):
    widget = widgets.CheckboxSelectMultiple
    form = BaseWidgetForm

class SplitDateTimeWidget(BaseWidget):
    widget = widgets.SplitDateTimeWidget
    form = BaseWidgetForm

class SplitHiddenDateTimeWidget(BaseWidget):
    widgets = widgets.SplitHiddenDateTimeWidget
    form = BaseWidgetForm

