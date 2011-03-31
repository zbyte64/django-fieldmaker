from django import forms
from django.forms import widgets

from resource import field_registry

class BaseFieldForm(forms.Form):
    required = forms.BooleanField(default=True)
    label = forms.CharField()
    initial = forms.CharField()
    help_text = forms.CharField()

class BaseField(object):
    field = None
    identities = list()
    form = BaseFieldForm
    
    def create_field(self, data):
        return self.field(**data)
    
    def widget_choices(self):
        choices = list()
        for widget in field_registry.widgets.itervalues():
            if not widget.identities:
                choices.append(widget)
            else:
                for identity in widget.identities:
                    if identity in self.identities:
                        choices.append(widget)
                        break
        return choices

class BooleanField(BaseField):
    field = forms.BooleanField
    identities = ['BooleanField']

field_registry.register_field('BooleanField', BooleanField)

class CharFieldForm(BaseFieldForm):
    max_length = forms.IntegerField(required=False)
    min_length = forms.IntegerField(required=False)

class CharField(BaseField):
    form = CharFieldForm
    field = forms.CharField
    identities = ['CharField']

field_registry.register_field('CharField', CharField)

class ChoiceFieldForm(BaseFieldForm):
    choices = forms.CharField(widget=widgets.Textarea, help_text='each line to contain: "value","label"')

class ChoiceField(BaseField):
    form = ChoiceFieldForm
    field = forms.ChoiceField
    identities = ['ChoiceField']

    def create_field(self, data):
        data['choices'] = [row.split(',',1) for row in data['choices'].split('\n')]
        return self.field(**data)

field_registry.register_field('ChoiceField', ChoiceField)

class DateField(BaseField):
    field = forms.DateField
    identities = ['DateField']

field_registry.register_field('DateField', DateField)

class DateTimeField(BaseField):
    field = forms.DateTimeField
    identities = ['DateTimeField']

field_registry.register_field('DateTimeField', DateTimeField)

class DecimalFieldForm(BaseFieldForm):
    max_value = forms.IntegerField(required=False)
    min_value = forms.IntegerField(required=False)
    max_digits = forms.IntegerField(required=False)
    decimal_places = forms.IntegerField(required=False)

class DecimalField(BaseField):
    form = DecimalFieldForm
    field = forms.DecimalField
    identities = ['DecimalField']

field_registry.register_field('DecimalField', DecimalField)

class EmailField(CharField):
    field = forms.EmailField
    identities = ['EmailField']

field_registry.register_field('EmailField', EmailField)

class FloatFieldForm(BaseFieldForm):
    max_value = forms.IntegerField(required=False)
    min_value = forms.IntegerField(required=False)

class FloatField(BaseField):
    form = FloatFieldForm
    field = forms.FloatField
    identities = ['FloatField']

field_registry.register_field('FloatField', FloatField)

class IntegerFieldForm(BaseFieldForm):
    max_value = forms.IntegerField(required=False)
    min_value = forms.IntegerField(required=False)

class IntegerField(BaseField):
    form = IntegerFieldForm
    field = forms.IntegerField
    identities = ['IntegerField']

field_registry.register_field('IntegerField', IntegerField)

class IPAddressField(BaseField):
    field = forms.IPAddressField
    identities = ['IPAddressField']

field_registry.register_field('IPAddressField', IPAddressField)

class NullBooleanField(BaseField):
    field = forms.NullBooleanField
    identities = ['NullBooleanField']

field_registry.register_field('NullBooleanField', NullBooleanField)

class RegexFieldForm(CharFieldForm):
    regex = forms.CharField()

class RegexField(BaseField):
    form = RegexFieldForm
    field = forms.RegexField
    identities = ['RegexField']

field_registry.register_field('RegexField', RegexField)

class SlugField(BaseField):
    field = forms.SlugField
    identities = ['SlugField']

field_registry.register_field('SlugField', SlugField)

class TimeField(BaseField):
    field = forms.TimeField
    identities = ['TimeField']

field_registry.register_field('TimeField', TimeField)

class URLFieldForm(BaseFieldForm):
    max_length = forms.IntegerField(required=False)
    min_length = forms.IntegerField(required=False)
    verify_exits = forms.BooleanField(default=False, required=False)
    validator_user_agent = forms.CharField(required=False)

class URLField(BaseField):
    form = URLFieldForm
    field = forms.URLField
    identities = ['URLField']

field_registry.register_field('URLField', URLField)

