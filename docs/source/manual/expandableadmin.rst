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

