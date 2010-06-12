"""Reports base class. This reports module trys to provide an ORM agnostic reports engine that will allow nice reports to be generated and exportable in a variety of formats. It seeks to be easy to use with querysets, raw SQL, or pure python. An additional goal is to have the reports be managed by model instances as well (e.g. a generic SQL based report that can be done in the backend).

"""

class Report(object):
    verbose_name="Abstract Report"
    available_filters={} #{"a filter":(('A','a'),('B','b'))}

    def __init__(self,request):
        self.request=request

    # CONSIDER maybe an "update rows"?
    def get_rows(self,filters={},order_by=None,page=0,page_length=-1):
        """takes in parameters and pumps out an iterable of iterables for rows/cols, an list of tuples with (name/value) for the aggregates"""
        return [],(('total',0),)

