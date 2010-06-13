from django.db import models

HELP_TEXT="""Raw SQL to run. Follows standard python string substitution (e.g. %(name)s). Variables passed in are order_by, page, per_page, and all filter parameters. NOTE: This is for skilled users only, and access should be restricted and monitored as severe dataloss and corruption can occur if used improperly."""

# TODO figure out how to make this read-only
class SQLReport(models.Model):
    sql=models.TextField(help_text=HELP_TEXT)

    # TODO add parameters to this that make it useful
