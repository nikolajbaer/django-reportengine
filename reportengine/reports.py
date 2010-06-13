import reportengine
from django.contrib.auth.models import User
from reportengine.filtercontrols import StartsWithFilterControl
from outputformats import *

class UserReport(reportengine.ModelReport):  
    """An example of a model report"""
    verbose_name = "User Report"
    slug = "user-report"
    namespace = "System"
    description = "Listing of all users in the system"
    labels = ('username','is_active','email','first_name','last_name','date_joined')
    list_filter=['is_active','date_joined',StartsWithFilterControl('username'),'groups']
    date_field = "date_joined" # Allows auto filtering by this date
    model=User
    per_page = 500

reportengine.register(UserReport)

class ActiveUserReport(reportengine.QuerySetReport):  
    """ An example of a queryset report. """
    verbose_name="Active User Report"
    slug = "active-user-report"
    namespace = "System"
    per_page=10
    labels = ('username','email','first_name','last_name','date_joined')
    queryset=User.objects.filter(is_active=True)

reportengine.register(ActiveUserReport)

class AppsReport(reportengine.Report):  
    """An Example report that is pure python, just returning a list"""
    verbose_name="Installed Apps"
    namespace = "System"
    slug = "apps-report"
    labels = ('app_name',)
    per_page = 0
    output_formats = [AdminOutputFormat(),XMLOutputFormat(root_tag="apps",row_tag="app")]

    def get_rows(self,filters={},order_by=None):
        from django.conf import settings
        # maybe show off by pulling active content type models for each app?
        # from django.contrib.contenttypes.models import ContentType
        apps=[[a,] for a in settings.INSTALLED_APPS]

        if order_by:
            # TODO add sorting based on label?
            apps.sort() 
        total=len(apps)
        return apps,(("total",total),)
 
reportengine.register(AppsReport)

class AdminActivityReport(reportengine.SQLReport):
    row_sql="""select username,user_id,count(*),min(action_time),max(action_time) 
            from django_admin_log 
            inner join auth_user on auth_user.id = django_admin_log.user_id 
            where is_staff = 1
            group by user_id;
    """
    aggregate_sql="""select avg(count) as average,max(count) as max,min(count) as min
            from (
                select count(user_id) as count 
                    from django_admin_log 
                    group by user_id
            )"""
    # TODO adding parameters to the sql report is.. hard.
    #query_params = [("username","Username","char")]
    namespace="Administration"
    labels = ('username','user id','actions','oldest','latest')
    verbose_name="Admin Activity Report"
    slug="admin-activity"

reportengine.register(AdminActivityReport)

