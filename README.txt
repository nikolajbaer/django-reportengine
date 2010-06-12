ReportEngine (for Django 1.1+)

Inspired by vitalik's django-reporting, ReportEngine seeks to make something less tied to the ORM to allow for those many instances where complex reports require some direct sql, or pure python code.

Also another goal is making it possible to expose reports in various formats (e.g. xml, csv).

Short Term:
TODO: add admin style filter controls
TODO: build SQLReport that is based on instances configured in backend
TODO: build CSV and XML exports
TODO: add namespacing and/or categorization for registering reports
TODO: add manage.py command that generates specified reports and puts them in a certain spot
TODO: add calendar view for date ranged reports

Long Term:
TODO: build xml file for exporting permissions to Google SDC for secure google spreadsheet importing
TODO: Add oauth for outside report gathering/pulling

