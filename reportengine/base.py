"""Reports base class. This reports module trys to provide an ORM agnostic reports engine that will allow nice reports to be generated and exportable in a variety of formats. It seeks to be easy to use with querysets, raw SQL, or pure python. An additional goal is to have the reports be managed by model instances as well (e.g. a generic SQL based report that can be done in the backend).

"""

class Report(object):
    verbose_name="Abstract Report"
    available_filters={} #{"a filter":(('A','a'),('B','b'))}
    labels = None
    daterange_filter = None # Set this to a filter variable to auto-range for calendar view
    # CONSIDER for orm we would use datevar__lte=DATE1&datevar__gte=DATE2 .. but not for non orm views.. so they need to parse this? Maybe a set_date_range function. if that function exists then we go ahead and show it . .and rely on the set_date_range to setup the report? Need something reasonable here.

    # CONSIDER maybe an "update rows"?
    def get_rows(self,filters={},order_by=None,page=0,page_length=-1):
        """takes in parameters and pumps out an iterable of iterables for rows/cols, an list of tuples with (name/value) for the aggregates"""
        return [],(('total',0),)

class QuerySetReport(Report):
    available_filters = {} # TODO: make this pull from admin?
    labels = None
    queryset = None

    def get_rows(self,filters={},order_by=None,page=0,page_length=None):
        qs=self.queryset.filter(**filters)
        if order_by:
            qs=qs.order_by(order_by)
        if page_length:
           qs=qs[page*page_length:(page+1)*page_length]
        return qs.values_list(*self.labels),(("total",qs.count()),)

class ModelReport(QuerySetReport):
    model = None

    def __init__(self):
        super(ModelReport,self).__init__() 
        self.queryset=self.model.objects

