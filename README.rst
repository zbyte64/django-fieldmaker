===========================================
django-fieldmaker - Form Creator for Django
===========================================

:version: alpha

Introduction
============

This package enables you to design forms in the Django admin. Other libraries may register new fields or widgets for the designer to use.


To use you first have to add ``fieldmaker`` to ``INSTALLED_APPS``, and then
execute ``syncdb`` to create the tables.


Using Expandable Forms
======================

``ExpandableForm`` and ``ExpandableModelForm`` allow you to define forms and have the user expand those forms through the admin.
The form will add any fields defined in the form definition having the form_key specified in the Meta. The ExpandableModelForm will additionally save the extra information and associate it to the instance.

Example usage::

    from django import forms
    from fieldmaker.forms import ExpandableForm, ExplandableModelForm
    from myapp.models import MyModel
    
    class MyForm(ExpandableForm):
        title = forms.CharField()
        
        class Meta:
            form_key = 'myform'
    
    class MyModelForm(ExpandableModelForm):
        class Meta:
            model = MyModel
            form_key = 'mymodel'


Extending Your Admin
====================

``ExpandableModelAdmin`` allows for forms in the admin to have fields dynamically defined and added to them. 
If a ModelAdmin that inherits from this class is registered in the admin, then creating a form definition with the key <app_label>_<object_name> and adding fields will add fields you your admin.

Adding a form definition using the admin with the key "myapp_mymodel" would add dynamically fields to the MyModel admin below::

    from django.contrib import admin
    from fieldmaker.admin import ExpandableModelAdmin
    
    from myapp.models import MyModel
    
    class MyModelAdmin(ExpandableModelAdmin):
        pass
    
    admin.site.register(MyModel, MyModelAdmin)


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


License
=======

This software is licensed under the ``New BSD License``. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround

