from datetime import datetime
import csv

from django.http import HttpResponse

from main.utils import rgetattr

from boms.models import BOM, BOMItem
from logical_parts.models import LogicalPart
from logical_part_links.models import LogicalPart2ManufacturerPart
from manufacturer_parts.models import ManufacturerPart
from supplier_parts.models import SupplierPart
from part_categories.models import PartCategory
from part_notes.models import PartNote
from part_units.models import PartUnit
from organizations.models import Organization

def backup(request):

    def prep(qs, fields):
        head = [t[0] for t in fields]
        body = []
        for obj in qs:
            row = []
            for field in fields:
                value = rgetattr(obj, field[1])
                if str(type(value)) == "<class 'int'>":
                    value = str(value)
                elif str(type(value)) == "<class 'bool'>":
                    value = 'True' if value else 'False'
                elif str(type(value)) == "<class 'datetime.datetime'>":
                    value = value.strftime('%Y-%m-%d_%H:%M:%S.%f')
                row.append(value)
            body.append(row)
        return head, body

    rows = []

    # organizations
    head, body = prep(Organization.objects.all().order_by('name'),
        [
            ('Org', 'name'),
            ('OrgM', 'manufacturer'),
            ('OrgS', 'supplier'),
            ('OrgURL', 'url'),
            ('OrgNotes', 'notes')
        ]
    )
    rows += [head] + body + [[]]

    # part units
    head, body = prep(PartUnit.objects.all().order_by('name'),
        [
            ('Unit', 'name'),
            ('UnitDesc', 'description')
        ]
    )
    rows += [head] + body + [[]]

    # part categories
    head, body = prep(PartCategory.objects.all().order_by('name'),
        [
            ('Cat', 'name'),
            ('CatDesc', 'description')
        ]
    )
    rows += [head] + body + [[]]

    # part notes
    head, body = prep(PartNote.objects.all().order_by('note'),
        [
            ('Note', 'note')
        ]
    )
    rows += [head] + body + [[]]

    # logical parts
    head, body = prep(LogicalPart.objects.all().order_by('part_number')
        .select_related('category')
        .order_by('category__name', 'part_number'),
        [
            ('Cat', 'category__name'),
            ('LPN', 'part_number'),
            ('LPDesc', 'description'),
            ('Note', 'notes__note')
        ]
    )
    rows += [head] + body + [[]]

    # manufacturer parts
    head, body = prep(ManufacturerPart.objects.all()
        .select_related('organization', 'category')
        .order_by('category__name', 'organization__name', 'part_number'),
        [
            ('Cat', 'category__name'),
            ('MPOrg', 'organization__name'),
            ('MPN', 'part_number'),
            ('MPDesc', 'description'),
            ('Unit', 'unit')
        ]
    )
    rows += [head] + body + [[]]

    # supplier parts
    head, body = prep(SupplierPart.objects.all()
        .select_related('organization', 'category', 'manufacturer_part')
        .order_by('category__name', 'organization__name', 'part_number'),
        [
            ('Cat', 'category__name'),
            ('SPOrg', 'organization__name'),
            ('SPN', 'part_number'),
            ('SPDesc', 'description'),
            ('MPOrg', 'manufacturer_part__organization__name'),
            ('MPN', 'manufacturer_part__part_number'),
            ('MPQty', 'manufacturer_part_qty')
        ]
    )
    rows += [head] + body + [[]]

    # logical parts to manufacturer parts
    head, body = prep(LogicalPart2ManufacturerPart.objects.all()
        .select_related(
            'logical_part',
            'manufacturer_part',
            'manufacturer_part__organization'
        )
        .order_by(
            'manufacturer_part__organization__name',
            'manufacturer_part__part_number',
            'logical_part__part_number'
        ),
        [
            ('MPOrg',  'manufacturer_part__organization__name'),
            ('MPN',  'manufacturer_part__part_number'),
            ('LPN', 'logical_part__part_number')
        ]
    )
    rows += [head] + body + [[]]

    # BOMs
    head, body = prep(BOM.objects.all().order_by('name'),
        [
            ('BOM', 'name'),
            ('BOMDesc', 'description')
        ]
    )
    rows += [head] + body + [[]]

    # BOM items
    head, body = prep(BOMItem.objects.all()
        .select_related('bom', 'logical_part'),
        [
            ('BOM', 'bom__name'),
            ('LPN', 'logical_part__part_number'),
            ('Qty', 'quantity'),
            ('Refs', 'references')
        ]
    )
    rows += [head] + body + [[]]

    # respond
    response = HttpResponse(content_type='text/csv')
    csv.writer(response, dialect='excel').writerows(rows)
    response['Content-Disposition'] = 'attachment; filename="' + \
        'backup_' + datetime.now().strftime('%Y%m%d_%H%M%S.csv') + '"'
    return response