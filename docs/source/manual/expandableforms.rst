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
