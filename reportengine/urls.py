from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('reportengine.views',
    # Listing of reports
    url('^$', 'report_list', name='reports-list'),

    # view report redirected to current date format (requires date_field argument)
    url('^current/(?P<daterange>(day|week|month|year))/(?P<namespace>[-\w]+)/(?P<slug>[-\w]+)/$', 
        'current_redirect', name='reports-current'),
    # view report redirected to current date format with formatting specified
    url('^current/(?P<daterange>(day|week|month|year))/(?P<namespace>[-\w]+)/(?P<slug>[-\w]+)/(?P<output>[-\w]+)/$', 
        'current_redirect', name='reports-current-format'),
    # specify range of report per time (requires date_field)
    url('^date/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<namespace>[-\w]+)/(?P<slug>[-\w]+)/$', 
        'day_redirect', name='reports-date-range'),
    # specify range of report per time with formatting
    url('^date/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<namespace>[-\w]+)/(?P<slug>[-\w]+)/(?P<output>[-\w]+)/$', 
        'day_redirect', name='reports-date-range-format'),
    # Show latest calendar of all date accessible reports 
    url('^calendar/$', 'calendar_current_redirect', name='reports-calendar-current'),
    # Show specific month's calendar of reports
    url('^calendar/(?P<year>\d+)/(?P<month>\d+)/$', 'calendar_month_view', name='reports-calendar-month'),
    # Show specifi day's calendar of reports
    url('^calendar/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'calendar_day_view', name='reports-calendar-day'),

)

# Add async report view if we are doing async reports, otherwise go to sync report views
# NOTE i am doing this here in case we need to re-org the urls for future HTML compat. (my meta refresh is deprecated)
if hasattr(settings,"ASYNC_REPORTS") and settings.ASYNC_REPORTS:
    urlpatterns += patterns('reportengine.views',
        # TODO make this an option? to do async all the time?
        url('^view/(?P<namespace>[-\w]+)/(?P<slug>[-\w]+)/$', 'async_report', name='reports-view'),
        # view report in specified output format
        url('^view/(?P<namespace>[-\w]+)/(?P<slug>[-\w]+)/(?P<output>[-\w]+)/$', 'async_report', name='reports-view-format'),
    )    
else:
    urlpatterns += patterns('reportengine.views',
        # View report in first output style
        url('^view/(?P<namespace>[-\w]+)/(?P<slug>[-\w]+)/$', 'view_report', name='reports-view'),
        # view report in specified output format
        url('^view/(?P<namespace>[-\w]+)/(?P<slug>[-\w]+)/(?P<output>[-\w]+)/$', 'view_report', name='reports-view-format'),
    )


