from celery.decorators import task
from models import ReportRequest
import reportengine
from reportengine.outputformats import CSVOutputFormat, XMLOutputFormat
import StringIO
from urlparse import parse_qsl

# TODO not-DRY copy/paste from management/commands/generate_report.py, should be combined

class MockRequest(object):
    def __init__(self, **kwargs):
        self.REQUEST = kwargs

@task()
def async_report(token):
   
    try:
        repreq = ReportRequest.objects.get(token=token)
    except ReportRequest.DoesNotExist:
        # Error?
        return 


    kwargs = dict(parse_qsl(repreq.params)) 

    # THis is like 90% the same 
    reportengine.autodiscover() ## Populate the reportengine registry
    try:
        report = reportengine.get_report(repreq.namespace, repreq.slug)()
    except Exception, err:
        raise err  
    
    request = MockRequest(**kwargs)
    filter_form = report.get_filter_form(request)
    if filter_form.fields:
        if filter_form.is_valid():
            filters = filter_form.cleaned_data
        else:
            filters = {}
    else:
        if report.allow_unspecified_filters:
            filters = dict(request.REQUEST)
        else:
            filters = {}
    
    # Remove blank filters
    for k in filters.keys():
        if filters[k] == '':
            del filters[k]
    
    ## Update the mask and run the report!
    mask = report.get_default_mask()
    mask.update(filters)
    rows, aggregates = report.get_rows(mask, order_by=kwargs.get('order_by',None))
   
    output = StringIO.StringIO()
 
    ## Get our output format, setting a default if one wasn't set or isn't valid for this report
    outputformat = None
    oformat = kwargs.get("format",None)
    if oformat:
        for format in report.output_formats:
            if format.slug == oformat:
                outputformat = format

    if not outputformat:
        outputformat = report.output_formats[0]
    ## By default, [0] is AdminOutputFormat, so grab the last one instead
    #outputformat = report.output_formats[-1]
    
    context = {
        'report': report,
        'title': report.verbose_name,
        'rows': rows,
        'filter_form': filter_form,
        'aggregates': aggregates,
        'paginator': None,
        'cl': None,
        'page': 0,
        'urlparams': repreq.params
        }
    
    outputformat.generate_response(context, output)
    #output.close()
   
    repreq.content = output.getvalue() 
    repreq.save() 


