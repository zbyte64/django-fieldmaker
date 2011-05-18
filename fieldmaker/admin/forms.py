from django import forms

from django.contrib.admin import widgets as admin_widgets
from django.forms import widgets

from fieldmaker.resource import field_registry
from fieldmaker.spec_widget import FormWidget, ListFormField
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

class FieldEntryForm(forms.Form):
    name = forms.SlugField(required=True)
    field = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class':'vFieldSelectorField'}))
    field_spec = forms.CharField(required=False, widget=FormWidget(attrs={'class':'vFieldSpecField'}))
    widget = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class':'vWidgetSelectorField'}))
    widget_spec = forms.CharField(required=False, widget=FormWidget(attrs={'class':'vWidgetSpecField'}))
    
    def __init__(self, *args, **kwargs):
        super(FieldEntryForm, self).__init__(*args, **kwargs)
        self.populate_field_choices()
        self.populate_widget_choices()
        self.load_field_form()
        self.load_widget_form()
    
    def populate_field_choices(self):
        choices = field_registry.fields.keys()
        self.fields['field'].choices = [('', 'Select Field')] + zip(choices, choices)
    
    def populate_widget_choices(self):
        choices = field_registry.widgets.keys()
        self.fields['widget'].choices = [('', 'Select Widget')] + zip(choices, choices)
    
    def get_active_field_value(self, field_name):
        key = field_name
        if self.prefix:
            key = '%s-%s' % (self.prefix, key)
        
        value = mapping = None
        if field_name == 'widget':
            mapping = field_registry.widgets
        elif field_name == 'field':
            mapping = field_registry.fields
        
        if hasattr(self, 'cleaned_data') and value in self.cleaned_data:
            value = self.cleaned_data[field_name]
        elif self.data and key in self.data:
            value = self.data.get(key)
        if self.initial:
            value = self.initial.get(field_name)
        if value and mapping:
            value = mapping[value]
        return value
    
    def create_field_form(self):
        field = self.get_active_field_value('field')
        if not field: return
        form_cls = field.get_form()
        if self.prefix:
            prefix = '%s-field_spec' % self.prefix
        else:
            prefix = 'field_spec'
        
        self.fields['widget'].choices = [('', 'Select Widget')] + field.widget_choices()
        self.fields['widget'].initial = field.default_widget
        return form_cls(data=self.data or None, prefix=prefix, initial=self.initial.get('field_spec'))
    
    def create_widget_form(self):
        field = self.get_active_field_value('widget')
        if not field: return
        form_cls = field.get_form()
        if self.prefix:
            prefix = '%s-widget_spec' % self.prefix
        else:
            prefix = 'widget_spec'
        return form_cls(data=self.data or None, prefix=prefix, initial=self.initial.get('widget_spec'))
    
    def load_field_form(self):
        self.fields['field_spec'].widget.set_form(self.create_field_form())
    
    def load_widget_form(self):
        self.fields['widget_spec'].widget.set_form(self.create_widget_form())
    
    @property
    def field_form(self):
        return self.fields['field_spec'].widget.form
    
    @property
    def widget_form(self):
        return self.fields['widget_spec'].widget.form
    
    def clean(self):
        self.load_field_form()
        self.load_widget_form()
        if self.field_form:
            if self.field_form.is_valid():
                self.cleaned_data['field_spec'] = self.field_form.cleaned_data
            else:
                raise forms.ValidationError('Please fix your field')
        if self.widget_form:
            if self.widget_form.is_valid():
                self.cleaned_data['widget_spec'] = self.widget_form.cleaned_data
            else:
                raise forms.ValidationError('Please fix your widget')
        return self.cleaned_data

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
        for key, entry in field_registry.fields.iteritems():
            self.field_forms[key] = entry.render_for_admin(key)
        for key, entry in field_registry.widgets.iteritems():
            self.widget_forms[key] = entry.render_for_admin(key)
    
    def save(self, *args, **kwargs):
        instance = forms.ModelForm.save(self, *args, **kwargs)
        instance.set_data(self.cleaned_data['data'])
        return instance
    
    class Meta:
        model = FormDefinition

