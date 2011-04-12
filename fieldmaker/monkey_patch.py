from admin import ExpandableModelAdminMixin

def patch_model_admin(model_admin):
    if not isinstance(model_admin, type):
        model_admin = type(model_admin)
    if ExpandableModelAdminMixin not in model_admin.__bases__:
        new_bases = tuple([ExpandableModelAdminMixin] + list(model_admin.__bases__))
        model_admin.__bases__ = new_bases
    #TODO patch the form if it has one

