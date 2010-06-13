"""Reports base class. This reports module trys to provide an ORM agnostic reports engine that will allow nice reports to be generated and exportable in a variety of formats. It seeks to be easy to use with querysets, raw SQL, or pure python. An additional goal is to have the reports be managed by model instances as well (e.g. a generic SQL based report that can be done in the backend).

"""

class Report(object):
    verbose_name="Abstract Report"
    available_filters={} #{"a filter":(('A','a'),('B','b'))}
    labels = None
    per_page=100
    can_show_all=True

    def get_filter_forms(self,request):
        return []

    # CONSIDER maybe an "update rows"?
    # CONSIDER should paging be dealt with here to more intelligently handle aggregates?
    def get_rows(self,filters={},order_by=None):
        """takes in parameters and pumps out an iterable of iterables for rows/cols, an list of tuples with (name/value) for the aggregates"""
        return [],(('total',0),)

class QuerySetReport(Report):
    labels = None
    queryset = None
 
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

