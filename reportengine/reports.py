import reportengine
from django.contrib.auth.models import User
from reportengine.filtercontrols import StartsWithFilterControl

class UserReport(reportengine.ModelReport):  
    """An example of a model report"""
    verbose_name = "User Report"
    description = "Listing of all users in the system"
    labels = ('username','is_active','email','first_name','last_name','date_joined')
    list_filter=['is_active','date_joined',StartsWithFilterControl('username'),'groups']
    model=User
    per_page = 500

class ActiveUserReport(reportengine.QuerySetReport):  
    """ An example of a queryset report. """
    verbose_name="Active User Report"
    per_page=10
    labels = ('username','email','first_name','last_name','date_joined')
    queryset=User.objects.filter(is_active=True)

class AppsReport(reportengine.Report):  
    """An Example report that is pure python, just returning a list"""
    verbose_name="Installed Apps"
    labels = ('app_name',)
    per_page = 0

    def get_rows(self,filters={},order_by=None):
        from django.conf import settings
        # maybe show off by pulling active content type models for each app?
        # from django.contrib.contenttypes.models import ContentType
        apps=[[a,] for a in settings.INSTALLED_APPS]

        if order_by:
            # add sorting based on label?
            apps.sort() 
        total=len(apps)
        return apps,(("total",total),)
 
reportengine.register("user-report",UserReport)
reportengine.register("active-user-report",ActiveUserReport)
reportengine.register("apps-report",AppsReport)

