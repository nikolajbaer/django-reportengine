from django.shortcuts import render_to_response
from django.template.context import RequestContext
import reportengine

def report_list(request):
    r = reportengine.all_reports()
    return render_to_response('reportengine/list.html', {'reports': r}, 
                              context_instance=RequestContext(request))

def view_report(request, slug):
    report = reportengine.get_report(slug)(request)
    rows = report.get_rows() # TODO add all the parameters
    data = {'report': report, 'title':report.verbose_name,'rows':rows}
    return render_to_response('reportengine/view.html', data, 
                              context_instance=RequestContext(request))

