from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator
from django.contrib.admin.views.main import ALL_VAR,ORDER_VAR, PAGE_VAR
from django.contrib.admin.views.decorators import staff_member_required
import reportengine
from urllib import urlencode

# TODO add calendar view for date-ranged reports

# TODO Maybe use a class based view? how do i make it easy to build SQLReports?
@staff_member_required
def report_list(request):
    r = reportengine.all_reports()
    return render_to_response('reportengine/list.html', {'reports': r}, 
                              context_instance=RequestContext(request))

# TODO build date_field redirects.. so view is at /current/<day|week|month|year>/<slug>/<format>/ and redirects
# to the appropriate date filter
# TODO assign appropriate permissions. Some reports might need to be accessible via OAuth or some other mechanism
@staff_member_required
def view_report(request, slug, output=None):
    report = reportengine.get_report(slug)()
    params=dict(request.REQUEST)

    order_by=params.pop(ORDER_VAR,None)

    page,per_page=0,report.per_page
    try:
        page=int(params.pop(PAGE_VAR,0))
    except ValueError:
        pass # ignore bogus page/per_page

    # Filters are served as forms from the report
    filter_form=report.get_filter_form(request)
    if filter_form.fields:
        if filter_form.is_valid():
            filters=filter_form.cleaned_data
        else:
            # If invalid filters, blank out filters so form error can propagate up
            filters={}
    else:
        # If no filter form fields are present, we just allow params to go through
        # CONSIDER making this allowance explicit? e.g. report.allow_unspecified_filters
        if report.allow_unspecified_filters:
            filters=dict(request.REQUEST)
        else:
            filters={}

    # Remove blank filters
    for k in filters.keys():
        if filters[k] == '':
            del filters[k]

    # pull the rows and aggregates
    rows,aggregates = report.get_rows(filters,order_by=order_by)

    # Determine output format, as it can squash paging if it wants
    outputformat=None
    if output:
        for of in report.output_formats:
            if of.slug == output:
                outputformat=of
    if not outputformat:
        outputformat = report.output_formats[0] 

    # Fill out the paginator if we have specified a page length
    paginator=None
    cl=None
    if per_page and not outputformat.no_paging:
        paginator=Paginator(rows,per_page)
        p=paginator.page(page+1)
        rows=p.object_list

        # HACK: fill up a fake ChangeList object to use the admin paginator
        class MiniChangeList:
            def __init__(self,paginator,page,per_page,params):
                self.paginator=paginator
                self.page_num=page
                self.show_all=report.can_show_all
                self.can_show_all=False
                self.multi_page=True
                self.params=params

            def get_query_string(self,new_params=None,remove=None):
                # Do I need to deal with new_params/remove?
                if remove != None:
                    for k in remove:
                        del self.params[k]
                if new_params != None:
                    self.params.update(new_params)
                return "?%s"%urlencode(self.params)

        cl_params=order_by and dict(params,order_by=order_by) or params
        cl=MiniChangeList(paginator,page,per_page,cl_params)


    data = {'report': report, 
            'title':report.verbose_name,
            'rows':rows,
            'filter_form':filter_form,
            "aggregates":aggregates,
            "paginator":paginator,
            "cl":cl,
            "page":page,
            "urlparams":urlencode(request.REQUEST)}

    return outputformat.get_response(data,request)


