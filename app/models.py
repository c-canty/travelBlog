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
    # trip = models.ForeignKey('Trip', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

# class Trip(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.title
