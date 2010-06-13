"""Based loosely on admin filterspecs, these are more focused on delivering controls appropriate per field type

Different filter controls can be registered per field type. When assembling a set of filter controls, these field types will generate the appropriate set of fields. These controls will be based upon what is appropriate for that field. For instance, a datetimefield for filtering requires a start/end. A boolean field needs an "all", "true" or "false" in radio buttons.

"""
from django import forms
from django.db import models
from django.utils.translation import ugettext as _

# TODO build register and lookup functions
# TODO figure out how to manage filters and actual request params, which aren't always 1-to-1 (e.g. datetime)

class FilterControl(object):
    filter_controls=[]
    def __init__(self,field_name,label=None):
        self.field_name=field_name
        self.label=label         

    def get_fields(self):
        return {self.field_name:forms.CharField(label=self.label or self.field_name,required=False)}
    
    # Pulled from django.contrib.admin.filterspecs
    def register(cls, test, factory, datatype):
        cls.filter_controls.append((test, factory, datatype))
    register = classmethod(register)

    def create_from_modelfield(cls, f, field_name, label=None):
        for test, factory, datatype in cls.filter_controls:
            if test(f):
                return factory(field_name,label) 
    create_from_modelfield = classmethod(create_from_modelfield)

    def create_from_datatype(cls, datatype, field_name, label=None):
        for test, factory, dt in cls.filter_controls:
            if dt == datatype:
                return factory(field_name,label) 
    create_from_datatype = classmethod(create_from_datatype)

FilterControl.register(lambda m: isinstance(m,models.CharField),FilterControl,"char")

class DateTimeFilterControl(FilterControl):
    def get_fields(self):
        ln=self.label or self.field_name 
        start=forms.CharField(label=_("%s From")%ln,required=False,widget=forms.DateTimeInput())
        end=forms.CharField(label=_("%s To")%ln,required=False,widget=forms.DateTimeInput())
        return {"%s__gte"%self.field_name:start,"%s__lte"%self.field_name:end}

FilterControl.register(lambda m: isinstance(m,models.DateTimeField),DateTimeFilterControl,"datetime")

class BooleanFilterControl(FilterControl):
    def get_fields(self):
        return {self.field_name:forms.CharField(label=self.label or self.field_name,
                required=False,widget=forms.RadioSelect(choices=(('','All'),('1','True'),('0','False'))),initial='A')}

FilterControl.register(lambda m: isinstance(m,models.BooleanField),BooleanFilterControl,"boolean")

# TODO How do I register this one?
class StartsWithFilterControl(FilterControl):
    def get_fields(self):
        return {"%s__startswith"%self.field_name:forms.CharField(label=_("%s Starts With")%(self.label or self.field_name),
                required=False)}

