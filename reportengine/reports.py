import reportengine
from django.contrib.auth.models import User

class UserReport(reportengine.ModelReport):  
    verbose_name="User Report"
    available_filters = {"is_active":(('True','True'),('False','False'))}
    labels = ('username','is_active','email','first_name','last_name')
    model=User

class ActiveUserReport(reportengine.QuerySetReport):  
    verbose_name="Active User Report"
    available_filters = {}
    labels = ('username','email','first_name','last_name')
    queryset=User.objects.filter(is_active=True)

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
 
reportengine.register("user-report",UserReport)
reportengine.register("active-user-report",ActiveUserReport)
reportengine.register("apps-report",AppsReport)

