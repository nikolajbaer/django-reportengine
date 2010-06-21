"""Reports base class. This reports module trys to provide an ORM agnostic reports engine that will allow nice reports to be generated and exportable in a variety of formats. It seeks to be easy to use with querysets, raw SQL, or pure python. An additional goal is to have the reports be managed by model instances as well (e.g. a generic SQL based report that can be done in the backend).

"""
from django import forms 
from django.db import models
from django.db.models.fields.related import RelatedField
from django.db.models.fields import FieldDoesNotExist
from filtercontrols import *
from outputformats import *
import datetime

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
    namespace = "Default"
    slug ="base"
    labels = None
    per_page=100
    can_show_all=True
    output_formats=[AdminOutputFormat(),CSVOutputFormat()]
    allow_unspecified_filters = False
    date_field = None  # if specified will lookup for this date field. .this is currently limited to queryset based lookups
    default_mask = {}  # a dict of filter default values. Can be callable

    # TODO add charts = [ {'name','type e.g. bar','data':(0,1,3) cols in table}]
    # then i can auto embed the charts at the top of the report based upon that data..

    def get_default_mask(self):
        """Builds default mask. The filter is merged with this to create the filter for the report. Items can be callable and will be resolved when called here (which should be at view time)."""
        m={}
        for k in self.default_mask.keys():
            v=self.default_mask[k]
            m[k] =  callable(v) and v() or v
        return m 

    def get_filter_form(self,request):
        form = forms.Form(data=request.REQUEST)
        return form

    # CONSIDER maybe an "update rows"?
    # CONSIDER should paging be dealt with here to more intelligently handle aggregates?
    def get_rows(self,filters={},order_by=None):
        """takes in parameters and pumps out an iterable of iterables for rows/cols, an list of tuples with (name/value) for the aggregates"""
        return [],(('total',0),)

class QuerySetReport(Report):
    # TODO make labels more addressable. now fixed to fields in model. what happens with relations?
    labels = None
    queryset = None
    list_filter = []

    def get_filter_form(self,request):
        """Retrieves naive filter based upon list_filter and the queryset model fields.. will not follow __ relations i think"""
        # TODO iterate through list filter and create appropriate widget and prefill from request
        form = forms.Form(data=request.REQUEST)
        for f in self.list_filter:
            # Allow specification of custom filter control, or specify field name (and label?)
            if isinstance(f,FilterControl):
                control=f
            else:
                mfi,mfm=get_lookup_field(self.queryset.model,self.queryset.model,f)
                # TODO allow label as param 2
                control = FilterControl.create_from_modelfield(mfi,f)
            if control:
                fields = control.get_fields()
                form.fields.update(fields)
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

class SQLReport(Report):
    rows_sql=None # sql statement with named  parameters in python syntax (e.g. "%(age)s" )
    aggregate_sql=None # sql statement that brings in aggregates. pulls from column name and value for first row only 
    query_params=[] # list of tuples, (name,label,datatype) where datatype is a mapping to a registerd filtercontrol

    def get_filter_form(self,request):
        form=forms.Form(data=request.REQUEST) 
        for q in self.query_params:
            control = FilterControl.create_from_datatype(q[2],q[0],q[1])
            fields = control.get_fields()
            form.fields.update(fields)
        form.full_clean()
        return form

    # CONSIDER not ideal in terms paging, would be better to fetch within a range.. 
    def get_rows(self,filters={},order_by=None):
        # TODO incorporate offset/limit somehow
        from django.db import connection
        cursor = connection.cursor()
        if self.row_sql:
            cursor.execute(self.row_sql%filters) 
            rows=cursor.fetchall()
        else: rows=[]

        if self.aggregate_sql:
            cursor.execute(self.aggregate_sql%filters)
            result=cursor.fetchone() # only fetch first row
        
            agg=[]
            for i in range(len(result)):
                agg.append((cursor.description[i][0],result[i]))
        else: agg=[]

        return rows,agg
    
class DateSQLReport(SQLReport):
    aggregate_sql=None
    query_params=[("date","Date","datetime")]
    date_field="date"
    default_mask={
        "date__gte":lambda: (datetime.datetime.today() -datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
        "date__lt":lambda: (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
    }

# TODO build AnnotatedReport that deals with .annotate functions in ORM
