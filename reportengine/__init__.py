'''Duplicated from django-reporting by vitalik, but with my own twist -nb '''
import imp
from base import Report,ModelReport,QuerySetReport,SQLReport,DateSQLReport

# TODO  make this seperate from vitalik's registry methods
_registry = {}

def register(klass):
    _registry[(klass.namespace,klass.slug)] = klass

def get_report(namespace,slug):
    try:
        return _registry[(namespace,slug)]
    except KeyError:
        raise Exception("No such report '%s'" % slug)

def all_reports():
    return _registry.items()

def autodiscover():
    from django.conf import settings
    REPORTING_SOURCE_FILE =  getattr(settings, 'REPORTING_SOURCE_FILE', 'reports') 
    for app in settings.INSTALLED_APPS:
        try:
            app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
        except AttributeError:
            continue

        try:
            imp.find_module(REPORTING_SOURCE_FILE, app_path)
        except ImportError:
            continue
        __import__('%s.%s' % (app, REPORTING_SOURCE_FILE))


