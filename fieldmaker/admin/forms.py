from django import forms

from django.contrib.admin import widgets as admin_widgets
from django.forms import widgets

from fieldmaker.resource import registry
from fieldmaker.spec_widget import ListFormField, FieldEntryForm
from fieldmaker.forms import ExpandableModelForm
from fieldmaker.models import FormDefinition

#TODO review better methods of polishing admin integration
FORMWIDGET_FOR_FIELDMAKER_DEFAULTS = {
    widgets.DateTimeInput: {
        'form_class': forms.SplitDateTimeField,
        'widget': admin_widgets.AdminSplitDateTime
    },
    widgets.DateInput:       {'widget': admin_widgets.AdminDateWidget},
    widgets.TimeInput:       {'widget': admin_widgets.AdminTimeWidget},
    widgets.Textarea:       {'widget': admin_widgets.AdminTextareaWidget},
    #widgets.URLField:        {'widget': admin_widgets.AdminURLFieldWidget},
    #models.IntegerField:    {'widget': admin_widgets.AdminIntegerFieldWidget},
    widgets.TextInput:       {'widget': admin_widgets.AdminTextInputWidget},
    widgets.FileInput:       {'widget': admin_widgets.AdminFileWidget},
    widgets.ClearableFileInput:       {'widget': admin_widgets.AdminFileWidget},
}

class ExpandableAdminModelForm(ExpandableModelForm):
    def get_expanded_fields(self):
        fields = super(ExpandableAdminModelForm, self).get_expanded_fields()
        for key, field in fields.iteritems():
            widget_key = type(field.widget)
            if widget_key in FORMWIDGET_FOR_FIELDMAKER_DEFAULTS:
                field.widget = FORMWIDGET_FOR_FIELDMAKER_DEFAULTS[widget_key]['widget']()
        return fields

class AdminFormDefinitionForm(ExpandableAdminModelForm):
    data = ListFormField(form=FieldEntryForm)
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.install_expanded_fields()
        if self.instance and self.instance.pk:
            data = self.get_expanded_data(self.instance)
            self.initial.update(data)
            self.initial['data'] = self.instance.get_data()
        self.post_form_init()
        self.field_forms = dict()
        self.widget_forms = dict()
        for key, entry in self.get_form_spec().fields.iteritems():
            self.field_forms[key] = entry.render_for_admin(key)
        for key, entry in self.get_form_spec().widgets.iteritems():
            self.widget_forms[key] = entry.render_for_admin(key)
    
    def get_form_spec(self):
        return registry.form_specifications[self.fields['data'].form_cls.form_spec_version]
    
    def save(self, *args, **kwargs):
        instance = forms.ModelForm.save(self, *args, **kwargs)
        instance.set_data(self.cleaned_data['data'])
        return instance
    
    class Meta:
        model = FormDefinition

