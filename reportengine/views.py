from django.shortcuts import render_to_response
from django.template.context import RequestContext
import reportengine

# TODO add calendar view for date-ranged reports

# TODO Maybe use a class based view? how do i make it easy to build SQLReports?
def report_list(request):
    r = reportengine.all_reports()
    return render_to_response('reportengine/list.html', {'reports': r}, 
                              context_instance=RequestContext(request))

def view_report(request, slug):
    report = reportengine.get_report(slug)()
    params=dict(request.REQUEST)

    order_by=params.pop("order_by",None)

    # TODO add pager
    try:
        page=int(params.pop("page",0))
        page_length=int(params.pop("page_length",0))
    except ValueError:
        # ignore bogus page/page_length
        page,page_length=0,0

    # TODO put together filters here 
    filters=params

    rows,aggregates = report.get_rows(filters,order_by=order_by,page=page,page_length=page_length)
    data = {'report': report, 'title':report.verbose_name,'rows':rows,"aggregates":aggregates}

    return render_to_response('reportengine/view.html', data, 
                              context_instance=RequestContext(request))


