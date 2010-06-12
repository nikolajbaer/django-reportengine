from django.shortcuts import render_to_response
from django.template.context import RequestContext
import simplereports

def report_list(request):
    r = simplereports.all_reports()
    return render_to_response('simplereports/list.html', {'reports': r}, 
                              context_instance=RequestContext(request))

def view_report(request, slug):
    report = simplereports.get_report(slug)(request)
    rows = report.get_rows() # TODO add all the parameters
    data = {'report': report, 'title':report.verbose_name,'rows':rows}
    return render_to_response('simplereports/view.html', data, 
                              context_instance=RequestContext(request))

