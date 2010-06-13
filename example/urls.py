from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

# Be sure to autodiscover the reports
import reportengine
reportengine.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to',{"url":"/reports/"}),
    (r'^admin/', include(admin.site.urls)),
    (r'^reports/', include('reportengine.urls')),
)

