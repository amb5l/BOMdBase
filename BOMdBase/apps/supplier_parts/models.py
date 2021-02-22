from django.db import models

from part_categories.models import PartCategory
from manufacturer_parts.models import ManufacturerPart

class SupplierPart(models.Model):
    organization = models.ForeignKey( \
        'organizations.Organization',
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='supplier_parts')
    part_number = models.CharField(max_length=50)
    category = models.ForeignKey( \
        PartCategory,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='supplier_parts',
        related_query_name='supplier_part')
    description = models.CharField(max_length=100, blank=True)
    manufacturer_part = models.ForeignKey( \
        ManufacturerPart,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='supplier_parts',
        related_query_name='supplier_part')
    manufacturer_part_qty = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.organization.name + ' ' + self.part_number \
            if self.organization else '??? '+ self.part_number
    class Meta:
        models.UniqueConstraint( \
            fields=['organization','part_number'], name='unique')