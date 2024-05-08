"""
Definition of models.
"""

from django.db import models

# blog entry model
class BlogEntry(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
