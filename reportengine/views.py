from django.shortcuts import render_to_response,redirect
from django.template.context import RequestContext
from django.core.paginator import Paginator
from django.contrib.admin.views.main import ALL_VAR,ORDER_VAR, PAGE_VAR
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import reportengine
from urllib import urlencode
import datetime,calendar

def next_month(d):
    """helper to get next month"""
    return datetime.datetime(year=d.month<12 and d.year or d.year +1,month=d.month<12 and d.month+1 or 1,day=1)


# TODO Maybe use a class based view? how do i make it easy to build SQLReports?
@staff_member_required
def report_list(request):
    # TODO make sure to constrain based upon permissions
    reports = [{'namespace': r.namespace, 'slug': r.slug, 'verbose_name': r.verbose_name} \
            for s, r in reportengine.all_reports()]
    return render_to_response('reportengine/list.html', {'reports': reports},
                              context_instance=RequestContext(request))

# TODO build date_field redirects.. so view is at /current/<day|week|month|year>/<slug>/<format>/ and redirects
# to the appropriate date filter
# TODO assign appropriate permissions. Some reports might need to be accessible via OAuth or some other mechanism
@staff_member_required
def view_report(request, namespace, slug, output=None):
    report = reportengine.get_report(namespace,slug)()
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

    # Merge filters with default mask
    mask = report.get_default_mask()
    mask.update(filters)


    # pull the rows and aggregates
    rows,aggregates = report.get_rows(mask,order_by=order_by)

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

@staff_member_required
def current_redirect(request, daterange, namespace, slug, output=None):
    # TODO make month and year more intelligent per calendar
    days={"day":1,"week":7,"month":30,"year":365}
    d2=datetime.datetime.now()
    d1=d2 - datetime.timedelta(days=days[daterange])
    return redirect_report_on_date(request,d1,d2,namespace,slug,output)

@staff_member_required
def day_redirect(request, year, month, day, namespace, slug, output=None):
    year,month,day=int(year),int(month),int(day)
    d1=datetime.datetime(year=year,month=month,day=day)
    d2=d1 + datetime.timedelta(hours=24)
    return redirect_report_on_date(request,d1,d2,namespace,slug,output)

def redirect_report_on_date(request,start_day,end_day,namespace,slug,output=None):
    """Utility that allows for a redirect of a report based upon the date range to the appropriate filter"""
    report=reportengine.get_report(namespace,slug)
    params = dict(request.REQUEST)
    if report.date_field:
        # TODO this only works with model fields, needs to be more generic
        dates = {"%s__gte"%report.date_field:start_day,"%s__lt"%report.date_field:end_day}
        params.update(dates)
    if output:
        return HttpResponseRedirect("%s?%s"%(reverse("reports-view-format",args=[namespace,slug,output]),urlencode(params)))
    return HttpResponseRedirect("%s?%s"%(reverse("reports-view",args=[namespace,slug]),urlencode(params)))

@staff_member_required
def calendar_current_redirect(request):
    d=datetime.datetime.today()
    return redirect("reports-calendar-month",year=d.year,month=d.month)

@staff_member_required
def calendar_month_view(request, year, month):
    # TODO make sure to constrain based upon permissions
    # TODO find all date_field accessible reports
    year,month=int(year),int(month)
    reports=[r[1] for r in reportengine.all_reports() if r[1].date_field]
    date=datetime.datetime(year=year,month=month,day=1)
    prev_month=date-datetime.timedelta(days=1)
    nxt_month=next_month(date)
    cal=calendar.monthcalendar(year,month)
    # TODO possibly pull in date based aggregates?
    cx={"reports":reports,"date":date,"calendar":cal,"prev":prev_month,"next":nxt_month}
    return render_to_response("reportengine/calendar_month.html",cx,
                              context_instance=RequestContext(request))

@staff_member_required
def calendar_day_view(request, year, month,day):
    # TODO make sure to constrain based upon permissions
    # TODO find all date_field accessible reports
    year,month,day=int(year),int(month),int(day)
    reports=[r[1] for r in reportengine.all_reports() if r[1].date_field]
    date=datetime.datetime(year=year,month=month,day=day)
    cal=calendar.monthcalendar(year,month)
    # TODO possibly pull in date based aggregates?
    cx={"reports":reports,"date":date,"calendar":cal}
    return render_to_response("reportengine/calendar_day.html",cx,
                              context_instance=RequestContext(request))
