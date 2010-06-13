from django.conf.urls.defaults import *

urlpatterns = patterns('reportengine.views',
    url('^$', 'report_list', name='reports-list'),
    url('^view/(?P<namespace>[-\w]+)/(?P<slug>[-\w]+)/$', 'view_report', name='reports-view'),
    url('^view/(?P<namespace>[-\w]+)/(?P<slug>[-\w]+)/(?P<output>[-\w]+)/$', 'view_report', name='reports-view-format'),
    url('^current/(?P<daterange>(day|week|month|year))/(?P<namespace>[-\w]+)/(?P<slug>[-\w]+)/$', 
        'current_redirect', name='reports-current'),
    url('^current/(?P<daterange>(day|week|month|year))/(?P<namespace>[-\w]+)/(?P<slug>[-\w]+)/(?P<output>[-\w]+)/$', 
        'current_redirect', name='reports-current-format'),

)
