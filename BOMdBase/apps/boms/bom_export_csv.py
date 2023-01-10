from datetime import datetime
import csv

from django.db.models.functions import Lower
from django.http import HttpResponse

from .models import BOM, BOMItem

from main.utils import errmsg

def bom_export_csv(request, sort_xref):

    params = request.GET

    if 'bomid' not in params:
        return errmsg(request, 'BOM ID must be specified')
    bomid = params.get('bomid')
    if BOM.objects.filter(id=bomid).count() != 1:
        return errmsg(request, 'BOM not found in database')
    bom = BOM.objects.get(id=bomid)
    qs = BOMItem.objects.filter(bom=params.get('bomid')).all() \
        .select_related('logical_part') \
        .prefetch_related(
            'logical_part__manufacturer_parts',
            'logical_part__manufacturer_parts__manufacturer_part__supplier_parts'
        )
    if qs.count() == 0:
        return errmsg(request, 'No BOM items found in database')

    # sort
    print(sort_xref)
    if 'sort' in params:
        sort_fields = []
        for p in params.getlist('sort'):
            print(p)
            f = p.replace('-', '')
            if f in sort_xref:
                sort_fields.append(p.replace(f, sort_xref[f]))
        for i, s in enumerate(sort_fields):
            sort_fields[i] = Lower(s[1:]).desc() if s[0] == '-' else Lower(s)
        print(sort_fields)
        qs = qs.order_by(*sort_fields)

    # get max no. of manufacturer parts
    mp_max = 0
    for obj in qs:
        n = obj.logical_part.manufacturer_parts.count()
        if n > mp_max:
            mp_max = n

    # prepare to build rows
    rows = []

    # add header
    rows.append(['BOM:', bom.name])
    rows.append(['Description:', bom.description])
    row = [
        'Item',
        'Qty',
        'LPN',
        'LPDesc',
        'LPNotes'
    ]
    for i in range(1, 1+mp_max):
        row.append('Mfr' + str(i))
        row.append('MPN' + str(i))
    row.append('Refs')
    rows.append(row)

    # add body
    item = 1
    for obj in qs:
        row = [
            str(item),
            str(obj.quantity),
            obj.logical_part.part_number,
            obj.logical_part.description
        ]
        row.append(obj.logical_part.notes.note \
            if obj.logical_part.notes else ''
        )
        n = 0
        for lp2mp in obj.logical_part.manufacturer_parts.all():
            row.append(lp2mp.manufacturer_part.organization.name)
            row.append(lp2mp.manufacturer_part.part_number)
            n += 1
        for i in range(mp_max-n):
            row += ['', '']
        row.append(obj.references)
        rows.append(row)
        item += 1

    # return CSV
    response = HttpResponse(content_type='text/csv')
    csv.writer(response, dialect='excel').writerows(rows)
    response['Content-Disposition'] = 'attachment; filename="' + \
        'bom_' + bom.name + '_' + \
            datetime.now().strftime('%Y%m%d_%H%M%S.csv') + '"'
    return response