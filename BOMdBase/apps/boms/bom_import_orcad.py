import os
from io import StringIO
import re
from natsort import natsorted

from boms.models import BOM, BOMItem
from logical_parts.models import LogicalPart

def bom_import_orcad(bom_name, file, create_parts, dry_run):

    logtext = ''
    n = 0

    def log(text):
        nonlocal logtext
        logtext += text + '<br>\n'
        return logtext

    def logn(text):
        nonlocal logtext, n
        logtext += 'line %d: ' % n + text + '<br>\n'
        return logtext

    def get_next_line(r):
        nonlocal n
        l = None
        while not l:
            try:
                l = next(r).replace('\r', '').replace('\n', '')
                n += 1
            except StopIteration:
                return ''
        return l

    log('Starting import process for BOM: ' + bom_name)
    if dry_run and BOM.objects.filter(name=bom_name).count():
        log('WARNING: BOM already exists!')
    log('Reading from file: ' + file.name)

    reader = StringIO(file.read().decode('utf-8-sig'))

    # process title etc
    l = get_next_line(reader)
    if not l:
        return log('empty file')
    if not 'Revised:' in l:
        return logn('expected "Revised:"')
    p = re.compile(r'(.+)(  )(Revised: )(.+)')
    r = p.search(l)
    title, rev_date = r.group(1), r.group(4)
    if not title:
        return logn('could not extract title')
    if not rev_date:
        return logn('could not extract revised date')
    l = get_next_line(reader)
    if not l:
        return logn('file truncated')
    if not 'Revision:' in l:
        return logn('expected "Revision:"')
    p = re.compile(r'(\s+)(Revision: )(.+)')
    r = p.search(l)
    rev = r.group(3)
    if not rev:
        return logn('could not extract revision')
    l = get_next_line(reader)
    if not l:
        return logn('file truncated')
    if not 'Bill Of Materials' in l:
        return logn('expected "Bill of Materials"')
    p = re.compile(r'(Bill Of Materials)(\s+)(.+)(  )(\s+)(.+)(\s+)(Page)(.+)')
    r = p.search(l)
    bom_date, bom_time, page = r.group(3), r.group(6), r.group(9)
    if not bom_date:
        return logn('could not extract BOM date')
    if not bom_time:
        return logn('could not extract BOM time')
    if not page:
        return logn('could not extract BOM page')
    log('Title: ' + title + '  Revision: ' + rev + '  Revised: ' + rev_date)
    log('BOM generated on ' + bom_date + ' at ' + bom_time)
    bom_description = title + ' rev ' + rev + ' revised ' + rev_date
    bom_description += ' (imported from ' + file.name + ', '
    bom_description += 'generated ' + bom_date + ' ' + bom_time + ')'

    # process headers
    log('Processing header...')
    l = get_next_line(reader)
    if not l:
        return 'file truncated after line ' + str(n)
    l = l.replace('Quantity', 'Qty')
    l = l.replace('References', 'Ref')
    l = l.replace('Reference', 'Ref')
    l = l.replace('Refs', 'Ref')
    l = l.replace('Logical Part Number', 'LPN')
    l = l.replace('Logical Part', 'LPN')
    headers = l.split('\t')
    if 'Item' not in headers:
        return logn('cannot proceed without item number')
    if 'Qty' not in headers:
        return logn('cannot proceed without quantity')
    if 'LPN' not in headers:
        return logn('cannot proceed without logical part number (LPN)')
    if 'Ref' not in headers:
        return logn('cannot proceed without part references')
    if len(set(headers)) != len(headers):
        return logn('found duplicate headers')
    for header in headers:
        if header not in ['Item', 'Qty', 'Ref', 'LPN']:
            logn('ignoring header ' + header)
    l = get_next_line(reader)
    if not l:
        return 'file truncated after line ' + str(n)
    if not l.replace('_', '') == '':
        return logn('expected horizontal line')

    # process body
    log('Processing body...')
    bom_items = []
    expected_item = 0
    item = lpn = qty = refs = None
    while True:
        def getli(l,i):
            return l[i] if len(l) > i else ''
        l = get_next_line(reader)
        row = l.split('\t')
        next_item = getli(row, headers.index('Item'))
        if next_item or not l:
            if lpn:
                if qty and refs:
                    if qty != len(refs):
                        return logn(
                            'quantity (%d) does not match ref count (%d)' % \
                            (qty, len(refs))
                        )
                    if qty == 0:
                        return logn('zero quantity')
                if refs:
                    refs = ' '.join(natsorted(refs))
                bom_items.append((lpn, qty, refs))
            if not l:
                break
            expected_item += 1
            item = next_item
            if item != str(expected_item):
                return logn('unexpected item number')
            lpn = getli(row, headers.index('LPN'))
            if not lpn:
                return logn('logical part number is empty')
            qty = getli(row, headers.index('Qty'))
            if not qty:
                return logn('quantity is empty')
            qty = int(qty)
            refs = []
        refs += [e for e in row[headers.index('Ref')].split(',') if e]
    log(str(item) + ' items processed OK')
    log('Checking for non-existent logical parts:')
    nonexistent = 0
    for lpn, _, _ in bom_items:
        if LogicalPart.objects.filter(part_number=lpn).count() != 1:
            nonexistent += 1
            log(lpn)
    if nonexistent:
        log(str(nonexistent) + ' logical parts not found in database')
    else:
        log('All logical parts exist in database')

    # can we proceed?
    if dry_run:
        return log('Dry run requested: halting before data import')
    if nonexistent and not create_parts:
        return log('"Create Parts" option has not been selected' \
            ' - unable to proceed')
    if BOM.objects.filter(name=bom_name).count():
        return log('BOM already exists - unable to proceed')

    # create BOM
    bom = BOM(name=bom_name, description=bom_description)
    bom.save()

    # create items
    for lpn, qty, refs in bom_items:
        if LogicalPart.objects.filter(part_number=lpn).count():
            lp = LogicalPart.objects.get(part_number=lpn)
        else:
            lp = LogicalPart(
                part_number=lpn,
                description='created for BOM ' + bom_name
            )
            lp.save()
        o = BOMItem(bom=bom, logical_part=lp, quantity=qty, references=refs)
        o.save()

    return log('Import process completed')