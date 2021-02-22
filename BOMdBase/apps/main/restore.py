import csv
from io import StringIO

from django.shortcuts import render

from .shared import navbar1
from .forms import FileImportForm

from main.utils import done

from boms.models import BOM, BOMItem
from logical_parts.models import LogicalPart
from logical_part_links.models import LogicalPart2ManufacturerPart
from manufacturer_parts.models import ManufacturerPart
from supplier_parts.models import SupplierPart
from part_categories.models import PartCategory
from part_notes.models import PartNote
from part_units.models import PartUnit
from organizations.models import Organization

def data_import(file):

    logtext = ''
    i = 0
    errors = 0

    def log(text):
        nonlocal logtext, i
        logtext += 'row %d: ' % (i+1) + text + '<br>\n'

    def err(text):
        nonlocal logtext, i, errors
        logtext += 'row %d: ' % (i+1) + text + '<br>\n'
        errors += 1

    def make_u(d, f):
        r = {}
        for k, v in f.items():
            if v in d:
                if d[v]:
                    r[k] = d[v]
        return r

    def create_or_update(model, f, u={}):
        for k, v in f.items():
            if not v:
                return None
        u = {k:v.lower() == 'true' \
            if model._meta.get_field(k).get_internal_type() == 'BooleanField'
            else v for k, v in u.items()
        }
        n = model.objects.filter(**f|u).count()
        if n == 1: # no update required
            o = model.objects.get(**f|u)
            log('no change: ' + model.__name__ + ' - ' + str(o))
        else:
            o, created = model.objects.update_or_create(**f, defaults=u)
            if created:
                log('created ' + model.__name__ + ': ' + str(o))
            else:
                log('updated: ' + model.__name__ + ' - ' + str(o))
        return o

    def sx(s, i):
        return s + str(i) if i else s

    r = csv.reader(StringIO(file.read().decode('utf-8-sig')), delimiter=',')
    rows = [row for row in r]

    while i < len(rows):

        # skip empty row
        if not rows[i]:
            i += 1
            continue
        if not rows[i][0]:
            i += 1
            continue

        # get head
        head = [h for h in rows[i] if h] # trim empty headers
        log('header: ' + ', '.join(head))

        # check header names
        l = [
            'Org', 'OrgM', 'OrgS', 'OrgURL', 'OrgNotes',
            'Unit', 'UnitDesc',
            'Cat', 'CatDesc',
            'Note',
            'LPN', 'LPDesc',
            'MPOrg', 'MPN', 'MPDesc',
            'BOM', 'BOMDesc',
            'Qty', 'Refs'
        ]
        for n in range(10):
            for s in ['SPOrg', 'SPN', 'SPDesc', 'SPNotes', 'MPQty']:
                l.append(sx(s, n))
        for h in head:
            if h and h not in l:
                err('unknown header (' + h + ')')
                return logtext

        # check field combinations
        combinations = ( # these must go together
            ('MPOrg', 'MPN'),
            ('SPOrg', 'SPN')
        )
        for combination in combinations:
            if any(item in head for item in combination) \
            and not all(item in head for item in combination):
                err(','.join(combination) + ' all required')
                return logtext

        # check dependancy requirements
        dependancies = ( # dependee required if any depender present
            ('Org', ('OrgM', 'OrgS', 'OrgURL', 'OrgNotes')),
            ('Cat', ('CatDesc', )),
            ('Unit', ('UnitDesc', 'UnitNotes')),
            ('LPN', ('LPDesc', )),
            ('MPN', ('MPDesc', )),
            ('SPN', ('SPDesc', )),
            ('BOM', ('BOMDesc', 'BOMNotes')),
            ('BOM', ('Qty', 'Refs')),
            ('LPN', ('Qty', 'Refs'))
        )
        for dependee, dependers in dependancies:
            if any(item in head for item in dependers):
                if dependee not in head:
                    err(','.join(dependers) + ' depend on ' + dependee)
                    return logtext

        # check restricted data combinations
        if 'OrgName' in head:
            if any(item in head for item in
                ['Unit', 'Cat', 'LPN', 'MPN', 'SPN', 'BOM', 'Ref']
            ):
                err('cannot combine Organization with other data')
                return logtext

        # process rows
        i += 1
        while i < len(rows):

            if not rows[i]:
                break
            if not rows[i][0]:
                break

            d = dict(zip(head,rows[i][:len(head)])) # create row dict

            cat = note = unit = lp = mporg = mp = sporg = sp = None

            # organizations
            if 'Org' in head:

                f = {'name': d['Org']}
                u = make_u(d,
                    {
                        'manufacturer': 'OrgM',
                        'supplier': 'OrgS',
                        'url': 'OrgURL',
                        'notes': 'OrgNotes'
                    }
                )
                create_or_update(Organization, f, u)

            # part categories
            if 'Cat' in d:
                f = {'name': d['Cat']}
                u = make_u(d, {'description': 'CatDesc'})
                cat = create_or_update(PartCategory, f, u)

            # part notes
            if 'Note' in d:
                f = {'note': d['Note']}
                note = create_or_update(PartNote, f, {})

            # part units
            if 'Unit' in d:
                f = {'name': d['Unit']}
                u = make_u(d,
                    {'description': 'UnitDesc', 'notes': 'UnitNotes'}
                )
                unit = create_or_update(PartUnit, f, u)

            # logical parts
            if 'LPN' in d:
                f = {'part_number': d['LPN']}
                u = make_u(d, {'description': 'LPDesc'})
                if cat:
                    u['category'] = cat
                if note:
                    u['notes'] = note
                lp = create_or_update(LogicalPart, f, u)

            # manufacturer parts
            if 'MPN' in d:
                mporg = create_or_update(Organization, {'name': d['MPOrg']})
                f = {'organization': mporg, 'part_number': d['MPN']}
                u = make_u(d, {'description': 'MPDesc'})
                if cat:
                    u['category'] = cat
                if unit:
                    u['unit'] = unit
                if 'MPDesc' not in d and 'LPDesc' in d: # inherit
                    u['description'] = d['LPDesc']
                mp = create_or_update(ManufacturerPart, f, u)

            # supplier parts
            for n in range(10): # handle SPOrg1..9, SPN1..9 etc
                if sx('SPN', n) in d:
                    if d[sx('SPOrg', n)] and d[sx('SPN', n)]: # not empty
                        sporg = create_or_update(Organization,
                            {'name': d[sx('SPOrg', n)]})
                        f = {
                            'organization': sporg,
                            'part_number': d[sx('SPN', n)]
                        }
                        u = make_u(d, {
                            'description': sx('SPDesc', n),
                            'notes': sx('SPNotes', n),
                            'manufacturer_part_qty': sx('MPQty', n)
                        })
                        if cat:
                            u['category'] = cat
                        if sx('SPDesc', n) not in d: # inherit
                            if 'MPDesc' in d:
                                u['description'] = d['MPDesc']
                            elif 'LPDesc' in d:
                                u['description'] = d['LPDesc']
                        if mp:
                            u['manufacturer_part'] = mp
                        create_or_update(SupplierPart, f, u)

            # logical part 2 manufacturer part
            if lp and mp:
                f = {'logical_part': lp, 'manufacturer_part': mp}
                create_or_update(LogicalPart2ManufacturerPart, f)

            # BOMs
            if 'BOM' in d:
                f = {'name': d['BOM']}
                u = make_u(d, {'description': 'BOMDesc', 'notes': 'BOMNotes'})
                bom = create_or_update(BOM, f, u)

            # BOM items
            if 'Refs' in d: # => Refs, LPN and Instr present
                f = {
                    'bom': bom,
                    'logical_part': lp
                }
                u = make_u(d, {
                    'references': 'Refs',
                    'quantity': 'Qty',
                })
                create_or_update(BOMItem, f, u)

            i +=1

    return logtext + 'Done.'

def restore(request):
    if request.method == 'POST':
        form = FileImportForm(request.POST, request.FILES)
        if form.is_valid():
            if 'file' in request.FILES:
                log = data_import(request.FILES['file'])
                return done(request, 'Database Restore/Import', log, 1)
            else:
                return done(request, 'Database Restore/Import', 'No file specified', 1)
    else:
        form = FileImportForm()
    context = { \
        'title': 'Database Restore/Import',
        'navbar1': navbar1,
        'form': form,
        'form_action': '/restore/'
        }
    return render(request, 'base.html', context)