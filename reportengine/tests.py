"""
Report Engine Tests.
"""
from base import Report
from filtercontrols import FilterControl
from django.test import TestCase
from django import forms
import reportengine

class BasicTestReport(Report):
    """Test Report. set the rows an aggregate to test"""
    slug="test"        
    namespace="testing"
    verbose_name="Basic Test Report"

    def __init__(self,
                    rows=[ [1,2,3] ],
                    labels=["col1","col2","col3"],
                    aggregate = (('total',1),),
                    filterform = forms.Form() ):
        self.rows=rows
        self.labels=labels
        self.aggregate=aggregate
        self.filterform=filterform

    def get_rows(self,filters={},order_by=None):
        return self.rows,self.aggregate

    def get_filter_form(self,request):
        return self.filterform

class BasicReportTest(TestCase):
    def test_report_register(self):
        """
        Tests registering a report, and verifies report is now accessible
        """
        r=BasicTestReport()
        reportengine.register(r)
        assert(reportengine.get_report("testing","test") == r)
        found=False
        for rep in reportengine.all_reports():
            if rep[0] == (r.namespace,r.slug):
                assert(rep[1] == r)
                found=True
        assert(found)


