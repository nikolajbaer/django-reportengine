from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from django.utils.encoding import smart_unicode
import csv
from cStringIO import StringIO
from xml.etree import ElementTree as ET

class OutputFormat(object):
    verbose_name="Abstract Output Format"
    slug="output"
    no_paging=False

    def generate_output(self, context, output):
        ## output is expected to be a file-like object, be it Django Response,
        ## StringIO, file, or sys.stdout. Anything sith a .write method should do.
        raise NotImplemented("Use a subclass of OutputFormat.")

    def get_response(self,context,request):
        raise NotImplemented("Use a subclass of OutputFormat.")

class AdminOutputFormat(OutputFormat):
    verbose_name="Admin Report"
    slug="admin"

    def generate_output(self, context, output):
        raise NotImplemented("Not necessary for this output format")

    def get_response(self,context,request):
        context.update({"output_format":self})
        return render_to_response('reportengine/report.html', context,
                              context_instance=RequestContext(request))

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
            w.writerow([smart_unicode(x) for x in a])
        w.writerow( context["report"].labels)
        for r in context["rows"]:
            w.writerow([smart_unicode(x) for x in r])
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
