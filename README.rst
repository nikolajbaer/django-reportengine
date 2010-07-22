ReportEngine (for Django 1.1+)
==============================

by Nikolaj Baer for Web Cube CMS [http://www.webcubecms.com]
------------------------------------------------------------

*Version: Very Alpha*

Overview
--------

Inspired by vitalik's django-reporting [http://code.google.com/p/django-reporting], ReportEngine seeks to make something less tied to the ORM to allow for those many instances where complex reports require some direct sql, or pure python code.

It allows you to add new reports that either feed directly from a model, do their own custom SQL or run anything in python. Reports can be outputted into various formats, and you can specify new formats. Reports can have extensible filter controls, powered by a form (with premade ones for queryset and model based reports).

Example
-------

Take a look at the sample project and reports in the example folder. To run it you need to have Django 1.1.2 and reportengine on your PYTHONPATH.


