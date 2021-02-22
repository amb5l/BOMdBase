from django.db import models

from logical_parts.models import LogicalPart
from manufacturer_parts.models import ManufacturerPart

class LogicalPart2ManufacturerPart(models.Model):
    logical_part = models.ForeignKey( \
        LogicalPart,
        on_delete=models.PROTECT,
        related_name='manufacturer_parts',
        related_query_name='manufacturer_part')
    manufacturer_part = models.ForeignKey( \
        ManufacturerPart,
        on_delete=models.PROTECT,
        related_name='logical_parts',
        related_query_name='logical_part')
    def __str__(self):
        return \
            self.manufacturer_part.organization.name + '_' + \
            self.manufacturer_part.part_number + '_' + \
            self.logical_part.part_number
    class Meta:
        models.UniqueConstraint(
            fields=['logical_part', 'manufacturer_part'], name='unique'
        )