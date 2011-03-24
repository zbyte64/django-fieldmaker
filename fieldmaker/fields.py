from django import forms
from django.forms import widgets

from resource import field_registry

class BaseFieldForm(forms.Form)
    required = forms.BooleanField(default=True)
    label = forms.CharField()
    initial = forms.CharField()
    help_text = forms.CharField()
    #TODO widget selector
    
    field = None
    identities = list()
    
    def create_field(self):
        return self.field(**self.cleaned_data)
    
    def clean(self):
        try:
            self.create_field()
        except Exception, error:
            if getattr(error, 'args', None):
                raise forms.ValidationError(error.args[0])
            raise
        return self.cleaned_data
    
    def widget_choices(self):
        choices = list()
        for widget in field_registry.widgets.itervalues():
            for identity in widget.identities:
                if identity in self.identities:
                    choices.append(identity)
                    break
        return choices

class BooleanFieldForm(BaseFieldForm):
    field = BooleanField
    identities = ['BooleanField']

field_registry.register_field('BooleanField', BooleanFieldForm)

class CharFieldForm(BaseFieldForm):
    max_length = forms.IntegerField(required=False)
    min_length = forms.IntegerField(required=False)
    field = forms.CharField
    identities = ['CharField']

field_registry.register_field('CharField', CharFieldForm)

class ChoiceFieldForm(BaseFieldForm):
    choices = forms.CharField(widget=widgets.Textarea)

    field = forms.ChoiceField
    identities = ['ChoiceField']

    def create_field(self):
        kwargs = dict(self.cleaned_data)
        kwargs['choices'] = [row.split(',',1) for row in kwargs['choices'].split('\n')]
        return self.field(**kwargs)

field_registry.register_field('ChoiceField', ChoiceFieldForm)

class DateFieldForm(BaseFieldForm):
    field = forms.DateField
    identities = ['DateField']

field_registry.register_field('DateField', DateFieldForm)

class DateTimeFieldForm(BaseFieldForm):
    field = forms.DateTimeField
    identities = ['DateTimeField']

field_registry.register_field('DateTimeField', DateTimeFieldForm)

class DecimalFieldForm(BaseFieldForm):
    max_value = forms.IntegerField(required=False)
    min_value = forms.IntegerField(required=False)
    max_digits = forms.IntegerField(required=False)
    decimal_places = forms.IntegerField(required=False)
    field = forms.DecimalField
    identities = ['DecimalField']

field_registry.register_field('DecimalField', DecimalFieldForm)

class EmailFieldForm(CharFieldForm):
    field = forms.EmailField
    identities = ['EmailField']

field_registry.register_field('EmailField', EmailFieldForm)

class FloatFieldForm(BaseFieldForm):
    max_value = forms.IntegerField(required=False)
    min_value = forms.IntegerField(required=False)
    field = forms.FloatField
    identities = ['FloatField']

field_registry.register_field('FloatField', FloatFieldForm)

class IntegerFieldForm(BaseFieldForm):
    max_value = forms.IntegerField(required=False)
    min_value = forms.IntegerField(required=False)
    field = forms.IntegerField
    identities = ['IntegerField']

field_registry.register_field('IntegerField', IntegerFieldForm)

class IPAddressFieldForm(BaseFieldForm):
    field = forms.IPAddressField
    identities = ['IPAddressField']

field_registry.register_field('IPAddressField', IPAddressFieldForm)

class NullBooleanFieldForm(BaseFieldForm):
    field = forms.NullBooleanField
    identities = ['NullBooleanField']

field_registry.register_field('NullBooleanField', NullBooleanFieldForm)

class RegexFieldForm(CharFieldForm):
    regex = forms.CharField()
    
    field = forms.RegexField
    identities = ['RegexField']

field_registry.register_field('RegexField', RegexFieldForm)

class SlugFieldForm(BaseFieldForm):
    field = forms.SlugField
    identities = ['SlugField']

field_registry.register_field('SlugField', SlugFieldForm)

class TimeFieldForm(BaseFieldForm):
    field = forms.TimeField
    identities = ['TimeField']

field_registry.register_field('TimeField', TimeFieldForm)

class URLFieldForm(BaseFieldForm):
    max_length = forms.IntegerField(required=False)
    min_length = forms.IntegerField(required=False)
    verify_exits = forms.BooleanField(default=False, required=False)
    validator_user_agent = forms.CharField(required=False)
    field = forms.URLField
    identities = ['URLField']

field_registry.register_field('URLField', URLFieldForm)

