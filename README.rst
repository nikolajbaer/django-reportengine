ReportEngine (for Django 1.1+)
==============================

by Nikolaj Baer for Web Cube CMS [http://www.webcubecms.com]
------------------------------------------------------------

*Version: 1.0ish* (in production but still naive)

Overview
--------

Inspired by vitalik's django-reporting [http://code.google.com/p/django-reporting], ReportEngine seeks to make something less tied to the ORM to allow for those many instances where complex reports require some direct sql, or pure python code.

It allows you to add new reports that either feed directly from a model, do their own custom SQL or run anything in python. Reports can be outputted into various formats, and you can specify new formats. Reports can have extensible filter controls, powered by a form (with premade ones for queryset and model based reports).

Workflow
--------

As of datasets branch, the report engine works as follows:

The Report API will allow you to determine what report you want, with what filters, and in what format. This can be processed in a view, a task, a manage command, or pretty much anywhere else in code.::

    call generate_report(reportslug,filters,order_by,output_format):
        Lookup Report Object and instantiate
        get datasets(filters,order_by):
            Report object can generate one or more Datasets (columsn and aggregates)
        generate_report_result(datasets,report,outputformat) 
            Instantiates Outputformat and passes in datasets
            Outputformat renders the report 
        return ReportResult
    
The report result will have the actual content of the report (e.g. raw PDF data, CSV, HTML) and return that. This can then be sent as a HttpRespones in a view, emailed as an attachment, saved to a file, stored in a session, etc.

Things this does not address:

1. Paging is not being handled (need to re-gen the entire report)

Additional helpers:

1. Reports can return a filter Form object that provides a form interface for creating the filter.
2. There is an optional monthly_aggregates functoin to let you easily list the reports in a calendar format

Example
-------

Take a look at the sample project and reports in the example folder. To run it you need to have Django 1.1.2 and reportengine on your PYTHONPATH.


