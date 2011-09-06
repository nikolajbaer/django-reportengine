from django.db import models
import datetime

class ReportRequest(models.Model):
    """Session based report request. Report request is made, and the token for the request is stored in the session so only that user can access this report. Task system generates the report and drops it into "content". When content is no longer null, user sees full report and their session token is cleared."""
    # TODO consider cleanup (when should this be happening? after the request is made? What about caching? throttling?)
    namespace = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    params = models.TextField() # url encoded GET params
    request_made = models.DateTimeField(default=datetime.datetime.now)
    token = models.CharField(max_length=255)
    content = models.TextField()
    viewed_on = models.DateTimeField(null=True)
    mimetype = models.CharField(max_length=255,null=True)
    
