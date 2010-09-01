import reportengine
import sys
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from reportengine.outputformats import CSVOutputFormat, XMLOutputFormat
from urlparse import parse_qsl

## ASSUMPTIONS: We're running this from the command line, so we can ignore
## - AdminOutputFormat
## - pagination

## TODO: Be more DRY about how the report is generated, including
## outputformat selection and filters and context creation

class MockRequest(object):
    def __init__(self, **kwargs):
        self.REQUEST = kwargs

class Command(BaseCommand):
    help = 'Run a report'
    option_list = BaseCommand.option_list + (
        make_option('-n', '--namespace',
            dest='namespace',
            default=None,
            help='Report namespace'
            ),
        make_option('-r', '--report',
            dest='report',
            default=None,
            help='Name of report'
            ),
        make_option('-f', '--file',
            dest='file',
            default=None,
            help='Path to file (defaults to sys.stdout)'
            ),
        make_option('-o', '--format',
            dest='format',
            default='csv',
            help='Output format slug (csv, xml, etc)'
            ),
        make_option('-q', '--filter',
            dest='filter',
            default='',
            help='Filter args as a querystring (foo=bar&fizz=buzz)'
            ),
        make_option('-b', '--order-by',
            dest='order_by',
            default=None,
            help='Field to order the report by'
            ),
        )

    def handle(self, *args, **kwargs):
        if not kwargs['namespace'] or not kwargs['report']:
            raise CommandError('--namespace and --report are required')

        ## Try to open the file path if specified, default to sys.stdout if it wasn't
        if kwargs['file']:
            try:
                output = file(kwargs['file'], 'w')
            except Exception:
                raise CommandError('Could not open file path for writing')
        else:
            output = sys.stdout

        reportengine.autodiscover() ## Populate the reportengine registry
        try:
            report = reportengine.get_report(kwargs['namespace'], kwargs['report'])()
        except Exception, err:
            raise CommandError('Could not find report for (%(namespace)s, %(report)s)' % kwargs)


        ## Parse our filters
        request = MockRequest(**dict(parse_qsl(kwargs['filter'])))
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
        rows, aggregates = report.get_rows(mask, order_by=kwargs['order_by'])

        ## Get our output format, setting a default if one wasn't set or isn't valid for this report
        outputformat = None
        if output:
            for format in report.output_formats:
                if format.slug == kwargs['format']:
                    outputformat = format
        if not outputformat:
            ## By default, [0] is AdminOutputFormat, so grab the last one instead
            outputformat = report.output_formats[-1]

        context = {
            'report': report,
            'title': report.verbose_name,
            'rows': rows,
            'filter_form': filter_form,
            'aggregates': aggregates,
            'paginator': None,
            'cl': None,
            'page': 0,
            'urlparams': kwargs['filter']
            }

        outputformat.generate_output(context, output)
        output.close()

        sys.exit(0)
