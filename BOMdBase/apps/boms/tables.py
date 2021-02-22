from main.utils import icon

boms_table = {

    'head': (
        ('Name', 'name', 1),
        ('Description', 'desc', 1),
        ('edit', 'edit', 1),
        ('del', 'del', 1),
    ),

    'sort': {
        'name': 'name',
        'desc': 'description'
    },

    'hide': {
        'desc': 'Description'
    },

    'aliases': {
        'id':       (0, 'id'),
        'name':     (0, 'name'),
        'desc':     (0, 'description'),
        'edit':     icon('edit'),
        'del':      icon('delete'),
    },

    'body': (
        ('name', 'name', 'view BOM',     'interactive?', {'bomid': 'id'} ),
        ('desc', 'desc', '',             '',             None            ),
        ('edit',  'edit', 'edit BOM',    'edit?',        {'bomid': 'id'} ),
        ('del',   'del',  'delete BOM',  'delete?',      {'bomid': 'id'} )
    )
}

boms_interactive_table = {

    'head': (
        ('Item', 'item', 1),
        ('Qty', 'qty', 1),
        ('References', 'refs', 1),
        ('Logical Part', 'lp', (
            ('Cat', 'lpcat', 1),
            ('PN', 'lpn', 1),
            ('Description', 'lpdesc', 1),
            ('Notes', 'lpnote', 1)
        )),
        ('Manufacturer Part(s)', 'mp', (
            ('Mfr', 'mporg', 1),
            ('PN', 'mpn', 1),
            ('Description', 'mpdesc', 1)
        )),
        ('Supplier Part(s)', 'sp', (
            ('Supplier', 'sporg', 1),
            ('PN', 'spn', 1),
            ('Description', 'spdesc', 1)
        ))
    ),

    'sort': {
        'qty': 'quantity',
        'lpcat': 'logical_part__category__name',
        'lpn': 'logical_part__part_number',
        'lpdesc': 'logical_part__description',
        'lpnote': 'logical_part__notes__note'
    },

    'hide': {
        'refs': 'References',
        'lpdesc': 'Logical Part Description',
        'lpnote': 'Logical Part Notes',
        'mp': 'Manufacturer Part(s)',
        'mpdesc': 'Manufacturer Part Description',
        'sp': 'Supplier Part(s)',
        'spdesc': 'Supplier Part Description'
    },

    'relations': (
        'logical_part',
        'manufacturer_parts',
        'manufacturer_part',
        'supplier_parts'
    ),

    'aliases': {
        'bomid':    '?bom',
        'item':     '*incr1',
        'qty':      (0, 'quantity'),
        'refs':     (0, 'references'),
        'lpid':     (1, 'id'),
        'lpn':      (1, 'part_number'),
        'lpcid':    (1, 'category__id'),
        'lpcat':    (1, 'category__name'),
        'lpdesc':   (1, 'description'),
        'lpnote':   (1, 'notes__note'),
        'mpid':     (3, 'id'),
        'mpoid':    (3, 'organization__id'),
        'mporg':    (3, 'organization__name'),
        'mpn':      (3, 'part_number'),
        'mpdesc':   (3, 'description'),
        'spid':     (4, 'id'),
        'spoid':    (4, 'organization__id'),
        'sporg':    (4, 'organization__name'),
        'spn':      (4, 'part_number'),
        'spdesc':   (4, 'description')
    },

    'body': (
        ('item',   'item',   '',                          '',                     None    ),
        ('qty',    'qty',    '',                          '',                     None    ),
        ('refs',   'refs',   '',                          '',                     None    ),
        ('lpcat',  'lpcat',  'logical part category',     '/part_categories#',    'lpcid' ),
        ('lpn',    'lpn',    'logical part',              '/logical_parts#',      'lpid'  ),
        ('lpdesc', 'lpdesc', '',                          '',                     None    ),
        ('lpnote', 'lpnote', '',                          '',                     None    ),
        ('mporg',  'mporg',  'manufacturer organization', '/organizations#',      'mpoid' ),
        ('mpn',    'mpn',    'manufacturer part',         '/manufacturer_parts#', 'mpid'  ),
        ('mpdesc', 'mpdesc', '',                          '',                     None    ),
        ('sporg',  'sporg',  'supplier organization',     '/organizations#',      'spoid' ),
        ('spn',    'spn',    'supplier part',             '/supplier_parts#',     'spid'  ),
        ('spdesc', 'spdesc', '',                          '',                     None    )
    )
}

boms_printable_table = {

    'nolinks': True,

    'head': (
        ('Item', 'item', 1),
        ('Qty', 'qty', 1),
        ('References', 'refs', 1),
        ('Logical Part', 'lp', (
            ('Cat', 'lpcat', 1),
            ('PN', 'lpn', 1),
            ('Description', 'lpdesc', 1),
            ('Notes', 'lpnote', 1)
        )),
        ('Manufacturer Part(s)', 'mp', (
            ('Mfr', 'mporg', 1),
            ('PN', 'mpn', 1),
            ('Description', 'mpdesc', 1)
        )),
        ('Supplier Part(s)', 'sp', (
            ('Supplier', 'sporg', 1),
            ('PN', 'spn', 1),
            ('Description', 'spdesc', 1)
        ))
    ),

    'sort': {
        'qty': 'quantity',
        'lpcat': 'logical_part__category__name',
        'lpn': 'logical_part__part_number',
        'lpdesc': 'logical_part__description',
        'lpnote': 'logical_part__notes__note'
    },

    'hide': {
        'refs': 'References',
        'lpdesc': 'Logical Part Description',
        'lpnote': 'Logical Part Notes',
        'mp': 'Manufacturer Part(s)',
        'mpdesc': 'Manufacturer Part Description',
        'sp': 'Supplier Part(s)',
        'spdesc': 'Supplier Part Description'
   },

    'relations': (
        'logical_part',
        'manufacturer_parts',
        'manufacturer_part',
        'supplier_parts'
    ),

    'aliases': {
        'bomid':    '?bom',
        'item':     '*incr1',
        'qty':      (0, 'quantity'),
        'refs':     (0, 'references'),
        'lpid':     (1, 'id'),
        'lpn':      (1, 'part_number'),
        'lpcid':    (1, 'category__id'),
        'lpcat':    (1, 'category__name'),
        'lpdesc':   (1, 'description'),
        'lpnote':   (1, 'notes__note'),
        'mpid':     (3, 'id'),
        'mpoid':    (3, 'organization__id'),
        'mporg':    (3, 'organization__name'),
        'mpn':      (3, 'part_number'),
        'mpdesc':   (3, 'description'),
        'spid':     (4, 'id'),
        'spoid':    (4, 'organization__id'),
        'sporg':    (4, 'organization__name'),
        'spn':      (4, 'part_number'),
        'spdesc':   (4, 'description')
    },

    'body': (
        ('item',   'item',   '', '', None ),
        ('qty',    'qty',    '', '', None ),
        ('refs',   'refs',   '', '', None ),
        ('lpcat',  'lpcat',  '', '', None ),
        ('lpn',    'lpn',    '', '', None ),
        ('lpdesc', 'lpdesc', '', '', None ),
        ('lpnote', 'lpnote', '', '', None ),
        ('mporg',  'mporg',  '', '', None ),
        ('mpn',    'mpn',    '', '', None ),
        ('mpdesc', 'mpdesc', '', '', None ),
        ('sporg',  'sporg',  '', '', None ),
        ('spn',    'spn',    '', '', None ),
        ('spdesc', 'spdesc', '', '', None ),
    )
}