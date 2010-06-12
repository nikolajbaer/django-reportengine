import reportengine
from django.contrib.auth.models import User

# TODO don't name this reportengine
class UserReport(reportengine.Report):  
    verbose_name="User Report"
    available_filters = {"a filter":(('A','a'),('B','b'))}
    labels = ('username','is_active','email','first_name','last_name')

    def get_rows(self,filters={},order_by=None,page=0,page_length=None):
        qs=User.objects.filter(**filters)
        if order_by:
            qs=qs.order_by(order_by)
        if page_length:
           qs=qs[page*page_length:(page+1)*page_length]
        return qs.values_list(*self.labels),(("total",qs.count()),)


class AppsReport(reportengine.Report):  
    verbose_name="Installed Apps"
    available_filters = {}
    labels = ('app_name',)

    def get_rows(self,filters={},order_by=None,page=0,page_length=None):
        from django.conf import settings
        apps=[[a] for a in settings.INSTALLED_APPS]
        if order_by:
            # add sorting based on label?
            apps.sort() 
        total=len(apps)
        if page_length:
           apps=apps[page*page_length:(page+1)*page_length]
        return apps,(("total",total),)
 
reportengine.register("test-report",UserReport)
reportengine.register("apps-report",AppsReport)

