= ReportEngine (for Django 1.1+) =
by Nikolaj Baer for Web Cube CMS [http://www.webcubecms.com]

== Overview ==

Inspired by vitalik's django-reporting [http://code.google.com/p/django-reporting], ReportEngine seeks to make something less tied to the ORM to allow for those many instances where complex reports require some direct sql, or pure python code.

It allows you to add new reports that either feed directly from a model, do their own custom SQL or run anything in python. Reports can be outputted into various formats, and you can specify new formats. Reports can have extensible filter controls, powered by a form (with premade ones for queryset and model based reports).

== Tasks ==

=== Short Term ===

TODO: build SQLReport that is based on instances configured in backend
TODO: add namespacing and/or categorization for registering reports
TODO: add manage.py command that generates specified reports and puts them in a certain spot
TODO: add calendar view for date ranged reports
TODO: add table row sorting
TODO: figure out per page aggregates (right now that is not accessible in get_rows)
TODO: maybe allow fields in queryset report to be callable on the model?
TODO: look into group bys, try an example
TODO: create an intuitive filter system for non-queryset based reports
TODO: add a "today","this week","this month" hot link to the DateTimeFilterControl, maybe let it parse "today" as an ongoing 
today field.. so like ?date_joined__lte=today or something
TODO: add fine-grained permissions per report

=== Long Term ===

TODO: build xml file for exporting permissions to Google SDC for secure google spreadsheet importing
TODO: Add oauth for outside report gathering/pulling
TODO: Add support for embedded graphs and charts (maybe alternate output format that allows embedding?)
TODO: Create emailer model that allows you to specify a certain report+filter and have it emailed daily
