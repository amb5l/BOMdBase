from django.db import models

class PartNote(models.Model):
    note = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.note