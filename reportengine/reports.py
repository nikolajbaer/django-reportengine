import reportengine
from django.contrib.auth.models import User

class UserReport(reportengine.ModelReport):  
    verbose_name = "User Report"
    description = "Listing of all users in the system"
    labels = ('username','is_active','email','first_name','last_name')
    list_filter=['is_active']
    model=User
    per_page = 500

class ActiveUserReport(reportengine.QuerySetReport):  
    verbose_name="Active User Report"
    per_page=10
    labels = ('username','email','first_name','last_name')
    queryset=User.objects.filter(is_active=True)

class AppsReport(reportengine.Report):  
    verbose_name="Installed Apps"
    labels = ('app_name',)
    per_page = 0

    def get_rows(self,filters={},order_by=None):
        from django.conf import settings
        # maybe show off by pulling active content type models for each app?
        # from django.contrib.contenttypes.models import ContentType
        apps=[[a] for a in settings.INSTALLED_APPS]

        if order_by:
            # add sorting based on label?
            apps.sort() 
        total=len(apps)
        return apps,(("total",total),)
 
reportengine.register("user-report",UserReport)
reportengine.register("active-user-report",ActiveUserReport)
reportengine.register("apps-report",AppsReport)

