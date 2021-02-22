from django.db import models

from part_categories.models import PartCategory
from part_notes.models import PartNote

class LogicalPart(models.Model):
    part_number = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey( \
        PartCategory,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='logical_parts',
        related_query_name='logical_part')
    description = models.CharField(max_length=100, blank=True)
    notes = models.ForeignKey( \
        PartNote,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='logical_parts',
        related_query_name='logical_part')
    def __str__(self):
        return self.part_number