from django.contrib import admin
from models import FormDefinition, GenericObjectStore
from modelforms import FormDefinitionForm

class FormDefinitionAdmin(admin.ModelAdmin):
    form = FormDefinitionForm

admin.site.register(FormDefinition, FormDefinitionAdmin)
