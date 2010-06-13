"""Reports base class. This reports module trys to provide an ORM agnostic reports engine that will allow nice reports to be generated and exportable in a variety of formats. It seeks to be easy to use with querysets, raw SQL, or pure python. An additional goal is to have the reports be managed by model instances as well (e.g. a generic SQL based report that can be done in the backend).

"""
from django import forms 
from django.db import models
from django.db.models.fields.related import RelatedField
from django.db.models.fields import FieldDoesNotExist

# Pulled from vitalik's Django-reporting
def get_model_field(model, name):
    return model._meta.get_field(name)

# Based on vitalik's Django-reporting
def get_lookup_field(model, original, lookup):
    parts = lookup.split('__')
    field = get_model_field(model, parts[0])
    if not isinstance(field, RelatedField) or len(parts) == 1:
        return field,model
    rel_model = field.rel.to
    next_lookup = '__'.join(parts[1:])
    return get_lookup_field(rel_model, original, next_lookup)

class Report(object):
    verbose_name="Abstract Report"
    available_filters={} #{"a filter":(('A','a'),('B','b'))}
    labels = None
    per_page=100
    can_show_all=True

    def get_filter_form(self,request):
        return forms.Form(request.REQUEST) 

    # CONSIDER maybe an "update rows"?
    # CONSIDER should paging be dealt with here to more intelligently handle aggregates?
    def get_rows(self,filters={},order_by=None):
        """takes in parameters and pumps out an iterable of iterables for rows/cols, an list of tuples with (name/value) for the aggregates"""
        return [],(('total',0),)

class QuerySetReport(Report):
    labels = None
    queryset = None
    list_filter = []

    def get_filter_form(self,request):
        """Retrieves naive filter based upon list_filter and the queryset model fields.. will not follow __ relations i think"""
        # TODO iterate through list filter and create appropriate widget and prefill from request
        form = forms.Form(data=request.REQUEST)
        for f in self.list_filter:
            # TODO grab model field and parse date, number, relation and choices appropriately
            # TODO also want to respect subdividing field relations, e.g. user__group__in type things
            # CONSIDER using a pattern like filterspecs here
            #mfi=self.queryset.model._meta.get_field(f)
            mfi,mfm=get_lookup_field(self.queryset.model,self.queryset.model,f)

            if isinstance(mfi, models.DateField):
                # TODO this is just a raw date== kind of thing.. but we really want to shoe-horn in a range
                # widget for a date/time field..
                fi = forms.CharField(label=f,required=False,widget=forms.DateTimeInput())
            elif isinstance(mfi, models.BooleanField):
                # TODO this is an issue because unchecked means that this value is not there..
                # perhaps make it a radio with "All" "True" "False".. but how will that work.. 
                fi = forms.BooleanField(label=f,required=False)
            else:
                fi = forms.CharField(label=f,required=False)
            form.fields[f]=fi
        form.full_clean()
        return form
 
    def get_rows(self,filters={},order_by=None):
        qs=self.queryset.filter(**filters)
        if order_by:
            qs=qs.order_by(order_by)
        return qs.values_list(*self.labels),(("total",qs.count()),)

class ModelReport(QuerySetReport):
    model = None

    def __init__(self):
        super(ModelReport,self).__init__() 
        self.queryset=self.model.objects

