from main.utils import icon

supplier_parts_table = {

    'head': (
        ('Cat', 'spcat', 1),
        ('Organization', 'sporg', 1),
        ('Part Number', 'spn',  1),
        ('Description', 'spdesc', 1),
        ('', 'spout', 1),
        ('', 'spedit', 1),
        ('', 'spdel', 1),
        ('Manufacturer', 'mp', (
            ('', 'mplk', 1),
            ('Qty', 'mpqty', 1),
            ('Name', 'mporg', 1),
            ('Part Number', 'mpn', 1),
            ('Description', 'mpdesc', 1),
            ('', 'mpunlk', 1),
            ('', 'mpedit', 1),
            ('', 'mpout', 1)
        ))
    ),

    'sort': {
        'spcat': 'category__name',
        'sporg': 'organization__name',
        'spn': 'part_number',
        'spdesc': 'description',
        'mporg': 'manufacturer_part__organization__name',
        'mpn': 'manufacturer_part__part_number',
    },

    'hide': {
        'spcat': 'Category',
        'spdesc': 'Description',
        'mp': 'Manufacturer Part',
        'mpdesc': 'Manufacturer Part Description',
    },

    'aliases': {
        'spid':     (0, 'id'),
        'spoid':    (0, 'organization__id'),
        'sporg':    (0, 'organization__name'),
        'spn':      (0, 'part_number'),
        'spcatid':  (0, 'category__id'),
        'spcat':    (0, 'category__name'),
        'spdesc':   (0, 'description'),
        'spedit':   icon('edit'),
        'spdel':    icon('delete'),
        'spout':    icon('extlink'),
        'mpid':     (0, 'manufacturer_part__id'),
        'mpoid':    (0, 'manufacturer_part__organization__id'),
        'mporg':    (0, 'manufacturer_part__organization__name'),
        'mpn':      (0, 'manufacturer_part__part_number'),
        'mpdesc':   (0, 'manufacturer_part__description'),
        'mpqty':    (0, 'manufacturer_part_qty'),
        'mplk':     icon('link'),
        'mpunlk':   icon('unlink'),
        'mpedit':   icon('edit'),
        'mpout':    icon('extlink'),
    },

    'body': (
        ('spcat',   'spcat',   'category',                  '/part_categories/#',           'spcatid'        ),
        ('sporg',   'sporg',   'supplier organization',     '/organizations/#',             'spoid'          ),
        ('spn',     'spn',     '',                          '',                             None             ),
        ('spdesc',  'spdesc',  '',                          '',                             None             ),
        ('spedit',  'spedit',  'edit supplier part',        'edit/?',                       {'spid': 'spid'} ),
        ('spdel',   'spdel',   'delete supplier part',      'delete/?',                     {'spid': 'spid'} ),
        ('spout',   'spout',   'search supplier part',      'search/?',                     {'spid': 'spid'} ),
        ('mplk',    'mplk',    'link to manufacturer part', '/supplier_part_link/select/?', {'spid': 'spid'} ),
        ('mpqty',   'mpqty',   '',                          '',                             None             ),
        ('mporg',   'mporg',   'manufacturer organization', '/organizations/#',             'mpoid'          ),
        ('mpn',     'mpn',     'manufacturer part',         '/manufacturer_parts/#',        'mpid'           ),
        ('mpdesc',  'mpdesc',  '',                          '',                             None             ),
        ('mpunlk',  'mpunlk',  'unlink manufacturer part',  '/supplier_part_link/break/?', {'spid': 'spid'} ),
        ('mpedit',  'mpedit',  'edit manufacturer part',    '/manufacturer_parts/edit?',   {'mpid': 'mpid'} ),
        ('mpout',   'mpout',   'search manufacturer part',  '/manufacturer_parts/search?', {'mpid': 'mpid'} )
    )
}

supplier_part_link_table = {

    'head': (
        ('Cat', 'mpcat', 1),
        ('Organization', 'mporg', 1),
        ('Part Number', 'mpn',  1),
        ('Description', 'mpdesc', 1),
        ('Unit', 'mpunit', 1),
        ('Supplier', 'sp', (
            ('Qty', 'mpqty', 1),
            ('Name', 'sporg', 1),
            ('Part Number', 'spn', 1),
            ('Description', 'spdesc', 1),
        ))
    ),

    'sort': {
        'mpcat': 'category__name',
        'mporg': 'organization__name',
        'mpn': 'part_number',
        'mpdesc': 'description',
        'mpunit': 'unit__name',
    },

    'hide': {
        'mpcat': 'Category',
        'mpdesc': 'Description',
        'mpunit': 'Unit',
        'sp': 'Supplier Parts',
        'spdesc': 'Supplier Part Descriptions',
    },

    'relations': (
        'supplier_parts',        # level 1: SupplierPart (1:n)
    ),

    'aliases': {
        'spid':     '?spid',
        'mpid':     (0, 'id'),
        'mporg':    (0, 'organization__name'),
        'mpn':      (0, 'part_number'),
        'mpcat':    (0, 'category__name'),
        'mpdesc':   (0, 'description'),
        'mpunit':   (0, 'unit__name'),
        'sporg':    (1, 'organization__name'),
        'spn':      (1, 'part_number'),
        'spdesc':   (1, 'description'),
        'mpqty':    (1, 'manufacturer_part_qty')
    },

    'body': (
        ('mpcat',  'mpcat',  '', '', None),
        ('mporg',  'mporg',  '', '', None),
        ('mpn',    'mpn',
             'create link to this part',
             '/supplier_part_link/create/?',
             {'mpid': 'mpid', 'spid': 'spid'}
        ),
        ('mpdesc', 'mpdesc', '', '', None),
        ('mpunit', 'mpunit', '', '', None),
        ('mpqty',  'mpqty',  '', '', None),
        ('sporg',  'sporg',  '', '', None),
        ('spn',    'spn',    '', '', None),
        ('spdesc', 'spdesc', '', '', None)
    )
}



