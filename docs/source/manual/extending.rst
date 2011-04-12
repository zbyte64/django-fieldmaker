Extending Fieldmaker
====================

To register a new field::

    from fieldmaker.fields import BaseFieldForm, BaseField
    from fieldmaker.resources import field_registry

    class URLFieldForm(BaseFieldForm):
        max_length = forms.IntegerField(required=False)
        min_length = forms.IntegerField(required=False)
        verify_exits = forms.BooleanField(initial=False, required=False)
        validator_user_agent = forms.CharField(required=False)

    class URLField(BaseField):
        form = URLFieldForm
        field = forms.URLField
        identities = ['URLField']

    field_registry.register_field('URLField', URLField)


To register a new widget::

    from fieldmaker.widgets import BaseWidgetForm, BaseWidget
    from fieldmaker.resources import field_registry

    class PasswordInputWidgetForm(BaseWidgetForm):
        render_value = forms.BooleanField(required=False, initial=True)

    class PasswordInput(BaseWidget):
        widget = widgets.PasswordInput
        identities = ['CharField']

    field_registry.register_widget('PasswordInput', PasswordInput)
