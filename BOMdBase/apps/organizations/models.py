from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=50, unique=True)
    manufacturer = models.BooleanField(null=True, blank=True)
    supplier = models.BooleanField(null=True, blank=True)
    url = models.URLField(max_length=100, blank=True)
    notes = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.name