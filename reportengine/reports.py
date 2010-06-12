import simplereports
from django.contrib.auth.models import User

# TODO don't name this simplereports
class TestReport(simplereports.Report):  
    verbose_name="My Report"
    available_filters = {"a filter":(('A','a'),('B','b'))}
    labels = ('username','is_active','email','first_name','last_name')

    def get_rows(self,filters={},order_by=None,page=0,page_length=None):
        qs=User.objects.filter(**filters)
        if order_by:
            qs=qs.order_by(order_by)
        if page_length:
           qs=qs[page*page_length:(page+1)*page_length]
        return qs.values_list(*self.labels)

 
simplereports.register("test-report",TestReport)

