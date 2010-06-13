from django.conf.urls.defaults import *

urlpatterns = patterns('reportengine.views',
    url('^$', 'report_list', name='reports-list'),
    url('^(?P<slug>[-\w]+)/$', 'view_report', name='reports-view'),
    url('^(?P<slug>[-\w]+)/(?P<output>[-\w]+)/$', 'view_report', name='reports-view-format'),

)
