from django.db import models

from part_categories.models import PartCategory
from part_units.models import PartUnit

class ManufacturerPart(models.Model):
    organization = models.ForeignKey( \
        'organizations.Organization',
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='manufacturer_parts')
    part_number = models.CharField(max_length=50)
    category = models.ForeignKey( \
        PartCategory,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='manufacturer_parts',
        related_query_name='manufacturer_part')
    description = models.CharField(max_length=100, blank=True)
    unit = models.ForeignKey( \
        PartUnit,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='manufacturer_parts')
    def __str__(self):
        return self.organization.name + ' ' + self.part_number \
            if self.organization else '??? '+ self.part_number
    class Meta:
        models.UniqueConstraint( \
            fields=['organization','part_number'], name='unique')