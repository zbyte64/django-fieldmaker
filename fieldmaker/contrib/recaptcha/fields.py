from django import forms

from fieldmaker.fields import BaseField, BaseFieldForm
from fieldmaker.widgets import BaseWidget, BaseWidgetForm
from fieldmaker.resource import field_registry

import recaptcha

class RecaptchaFieldForm(BaseFieldForm):
    public_key = forms.CharField()
    private_key = forms.CharField()

class RecaptchaField(BaseField):
    form = RecaptchaFieldForm
    field = recaptcha.RecaptchaField
    identities = ['RecaptchaField']

field_registry.register_field('RecaptchaField', RecaptchaField)


RECAPTCHA_THEMES = ['red', 'white','blackglass', 'clean']
RECAPTCHA_LANGUAGES = ['en', 'nl', 'fr', 'de', 'pt', 're', 'es', 'tr']

class RecaptchaWidgetForm(BaseWidgetForm):
    theme = forms.ChoiceField(choices=zip(RECAPTCHA_THEMES, RECAPTCHA_THEMES), required=False)
    tabindex = forms.IntegerField(required=False)
    lang = forms.ChoiceField(choices=zip(RECAPTCHA_LANGUAGES, RECAPTCHA_LANGUAGES), label='language', required=False)

class RecaptchaWidget(BaseWidget):
    form = RecaptchaWidgetForm
    widget = recaptcha.RecaptchaWidget
    identities = ['RecaptchaField']

field_registry.register_widget('RecaptchaWidget', RecaptchaWidget)
