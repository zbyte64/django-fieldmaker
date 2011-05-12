Meta Form Fields
================


FormField
---------

``FormField`` is a django field that allows you to embed a form as a field. To work properly, the form must inherit from ``MetaForm`` (or use the MetaFormMixin).

Example usage::

    from django import forms
    from spec_widget import FormField, MetaForm
    
    class PersonForm(forms.Form):
        first_name = forms.CharField()
        last_name = forms.CharField()
    
    class PeopleForm(MetaForm):
        person_one = FormField(form=PersonForm)
        person_two = FormField(form=PersonForm)
    
    form = PeopleForm(data=data)
    if form.is_valid():
        print form.cleaned_data


ListFormField
-------------

``ListFormField`` works like FormField but instead allows for an array of objects. This works by producing a formset and using that as the form.

Example usage::

    from django import forms
    from spec_widget import ListFormField, MetaForm
    
    class PersonForm(forms.Form):
        first_name = forms.CharField()
        last_name = forms.CharField()
    
    class GroupForm(MetaForm):
        name = forms.CharField()
        people = ListFormField(form=PersonForm)
    
    form = PeopleForm(data=data)
    if form.is_valid():
        print form.cleaned_data

