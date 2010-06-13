from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
import csv
from xml.etree import ElementTree as ET

class OutputFormat(object):
    def get_response(self,context,request):
        raise Exception("Use a subclass of OutputFormat.")        

class AdminOutputFormat(OutputFormat):
    verbose_name="Admin Report"
    slug="admin"

    def get_response(self,context,request):
        context.update({"output_format":self})
        return render_to_response('reportengine/report.html', context, 
                              context_instance=RequestContext(request))

class CSVOutputFormat(OutputFormat):
    verbose_name="CSV (comma seperated value)"
    slug="csv"

    # CONSIDER perhaps I could use **kwargs, but it is nice to see quickly what is available..
    def __init__(self,quotechar='"',quoting=csv.QUOTE_MINIMAL,delimiter=',',lineterminator='\n'):
        self.quotechar=quotechar
        self.quoting=quoting
        self.delimiter=delimiter
        self.lineterminator=lineterminator

    def get_response(self,context,request):
        resp = HttpResponse(mimetype='text/csv')
        # CONSIDER maybe a "get_filename" from the report?
        resp['Content-Disposition'] = 'attachment; filename=%s.csv'%context['report'].slug
        w=csv.writer(resp,
                    delimiter=self.delimiter,
                    quotechar=self.quotechar,
                    quoting=self.quoting,
                    lineterminator=self.lineterminator)
        w.writerow( context["report"].labels)
        for r in context["rows"]:
            w.writerow(r) 
        return resp

class XMLOutputFormat(OutputFormat):
    verbose_name="XML"
    slug="xml"
    
    def __init__(self,root_tag="output",row_tag="entry"):
        self.root_tag=root_tag
        self.row_tag=row_tag

    def get_response(self,context,request):
        resp = HttpResponse(mimetype='text/xml')
        # CONSIDER maybe a "get_filename" from the report?
        resp['Content-Disposition'] = 'attachment; filename=%s.xml'%context['report'].slug
        root = ET.Element(self.root_tag) # CONSIDER maybe a nicer name or verbose name or something
        rows=context["rows"] 
        labels=context["report"].labels
        for r in rows:
            e=ET.SubElement(root,self.row_tag)
            for l in range(len(labels)):
                e1=ET.SubElement(e,labels[l])
                e1.text = r[l]
        tree=ET.ElementTree(root)
        tree.write(resp)
        return resp

