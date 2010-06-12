from django.conf.urls.defaults import *

urlpatterns = patterns('reportengine.views',
    url('^$', 'report_list', name='reports-list'),
    url('^(?P<slug>.*)/$', 'view_report', name='reports-view'),
)
