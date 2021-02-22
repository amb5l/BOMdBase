from django.db import models
from django.core.validators import MinValueValidator

from logical_parts.models import LogicalPart

class BOM(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name

class BOMItem(models.Model):
    bom = models.ForeignKey( \
        BOM,
        on_delete=models.CASCADE,
        related_name='items',
        related_query_name='item')
    logical_part =  models.ForeignKey( \
        LogicalPart,
        on_delete=models.PROTECT,
        related_name='bom_items',
        related_query_name='bom_item')
    quantity = models.IntegerField(validators = [MinValueValidator(1)])
    references = models.TextField(blank = True)
    def __str__(self):
        return self.bom.name + '_' + getattr(self.logical_part, 'part_number')
    class Meta:
        models.UniqueConstraint(
            fields=['bom', 'logical_part'], name='unique'
        )