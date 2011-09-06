from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from django.utils.encoding import smart_unicode
import csv
from cStringIO import StringIO
from xml.etree import ElementTree as ET
from urllib import urlencode

# TODO must be serializable! So we can do async and store somewhere
class ReportResult(object):
    """Report Result encapsulates the report data response. This should be following the render by an OutputFormat, and encodes the mimetype and some additional meta."""
    def __init__(self,title,content,page=1,pages=None,perpage=None,meta={},mimetype="text/text"): 
        self.title = title
        self.content = content
        self.mimetype = mimetype
        self.meta = meta # catchall for stuff i didn't figure out
        # CONSIDER should this be how paging works?
        self.page = page
        self.pages = pages
        self.perpage = perpage

class ReportResultHttpResponse(ReportResult):
    def __init__(self,title,response):         
        self.response=response
        self.title=title
        self.mimetype = response.get("Content-Type","text/text")
        self.content = response.content

class OutputFormat(object):
    verbose_name="Abstract Output Format"
    slug="output"
    no_paging=False

    # Should this have paging in it? Who should know about paging?
    def get_result(self,datasets):
        raise NotImplementedError("Return Report Result in your subclass") 

    #def get_response(self,context,request):
    #    raise Exception("Use a subclass of OutputFormat.")        

class AdminOutputFormat(OutputFormat):
    verbose_name="Admin Report"
    slug="admin"

    # extra is how we transfer over stuff like the request object to the items that can use it
    def get_result(self,datasets,report,extra={}): 
        # TODO make this support multiple data sets
        data = {'report': report, 
                'title':report.verbose_name,
                'rows':datasets[0].get_data(),
                'filter_form':report.get_filter_form(datasets[0].filters), # TODO Datasets.filters should support multiple filter forms in a formset!
                "aggregates":datasets[0].get_aggregates(),
                "paginator":extra["paginator"],  # TODO add paginator
                "cl":extra["cl"], # TODO what in the heck is this?
                "page":extra["page"], # TODO add page
                "urlparams":urlencode(extra["request"].REQUEST)} # TODO how dow transfer this info over?

        data.update({"output_format":self})
        response = render_to_response('reportengine/report.html', data)
        result = ReportResultHttpResponse(data["title"],response)
        return result
                                      #context_instance=RequestContext(request))
    def generate_output(self, context, output):
        raise NotImplemented("Not necessary for this output format")

class CSVOutputFormat(OutputFormat):
    verbose_name="CSV (comma separated value)"
    slug="csv"
    no_paging=True

    # CONSIDER perhaps I could use **kwargs, but it is nice to see quickly what is available..
    def __init__(self,quotechar='"',quoting=csv.QUOTE_MINIMAL,delimiter=',',lineterminator='\n'):
        self.quotechar=quotechar
        self.quoting=quoting
        self.delimiter=delimiter
        self.lineterminator=lineterminator

    def generate_output(self, context, output):
        w=csv.writer(output,
                    delimiter=self.delimiter,
                    quotechar=self.quotechar,
                    quoting=self.quoting,
                    lineterminator=self.lineterminator)
        for a in context["aggregates"]:
            w.writerow([smart_unicode(x).encode('utf8') for x in a])
        w.writerow( context["report"].labels)
        for r in context["rows"]:
            w.writerow([smart_unicode(x).encode('utf8') for x in r])
        return output

    def get_response(self,context,request):
        resp = HttpResponse(mimetype='text/csv')
        # CONSIDER maybe a "get_filename" from the report?
        resp['Content-Disposition'] = 'attachment; filename=%s.csv'%context['report'].slug
        self.generate_output(context, resp)
        return resp

class XMLOutputFormat(OutputFormat):
    verbose_name="XML"
    slug="xml"
    no_paging=True

    def __init__(self,root_tag="output",row_tag="entry",aggregate_tag="aggregate"):
        self.root_tag=root_tag
        self.row_tag=row_tag
        self.aggregate_tag=aggregate_tag

    def generate_output(self, context, output):
        root = ET.Element(self.root_tag) # CONSIDER maybe a nicer name or verbose name or something
        for a in context["aggregates"]:
            ae=ET.SubElement(root,self.aggregate_tag)
            ae.set("name",a[0])
            ae.text=smart_unicode(a[1])
        rows=context["rows"]
        labels=context["report"].labels
        for r in rows:
            e=ET.SubElement(root,self.row_tag)
            for l in range(len(labels)):
                e1=ET.SubElement(e,labels[l])
                e1.text = smart_unicode(r[l])
        tree=ET.ElementTree(root)
        tree.write(output)

    def get_response(self,context,request):
        resp = HttpResponse(mimetype='text/xml')
        # CONSIDER maybe a "get_filename" from the report?
        resp['Content-Disposition'] = 'attachment; filename=%s.xml'%context['report'].slug
        self.generate_output(context, resp)
        return resp
