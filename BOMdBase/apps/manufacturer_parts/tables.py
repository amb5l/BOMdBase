from main.utils import icon

manufacturer_parts_table = {

    'head': (
        ('Cat', 'mpcat', 1),
        ('Organization', 'mporg', 1),
        ('Part Number', 'mpn',  1),
        ('Description', 'mpdesc', 1),
        ('Unit', 'mpunit', 1),
        ('', 'mpedit', 1),
        ('', 'mpdel', 1),
        ('', 'mpout', 1),
        ('Supplier', 'sp', (
            ('', 'splk', 1),
            ('Qty', 'mpqty', 1),
            ('Name', 'sporg', 1),
            ('Part Number', 'spn', 1),
            ('Description', 'spdesc', 1),
            ('', 'spunlk', 1),
            ('', 'spedit', 1),
            ('', 'spout', 1)
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
        'mpid':     (0, 'id'),
        'mpoid':    (0, 'organization__id'),
        'mporg':    (0, 'organization__name'),
        'mpn':      (0, 'part_number'),
        'mpcatid':  (0, 'category__id'),
        'mpcat':    (0, 'category__name'),
        'mpdesc':   (0, 'description'),
        'mpuid':    (0, 'unit__id'),
        'mpunit':   (0, 'unit__name'),
        'mpedit':   icon('edit'),
        'mpdel':    icon('delete'),
        'mpout':    icon('extlink'),
        'spid':     (1, 'id'),
        'spoid':    (1, 'organization__id'),
        'sporg':    (1, 'organization__name'),
        'spn':      (1, 'part_number'),
        'spdesc':   (1, 'description'),
        'mpqty':    (1, 'manufacturer_part_qty'),
        'splk':     icon('link+'),
        'spunlk':   (1, '#' + icon('unlink')),
        'spedit':   (1, '#' + icon('edit')),
        'spout':    (1, '#' + icon('extlink')),
    },

    'body': (
        ('mpcat',  'mpcat',  'category',                  '/part_categories/#',                'mpcatid'                        ),
        ('mporg',  'mporg',  'manufacturer organization', '/organizations/#',                  'mpoid'                          ),
        ('mpn',    'mpn',    '',                          '',                                  None                             ),
        ('mpdesc', 'mpdesc', '',                          '',                                  None                             ),
        ('mpunit', 'mpunit', 'unit',                      '/part_units/#',                     'mpuid'                          ),
        ('mpedit', 'mpedit', 'edit manufacturer part',    'edit/?',                            {'mpid': 'mpid'}                 ),
        ('mpdel',  'mpdel',  'delete manufacturer part',  'delete/?',                          {'mpid': 'mpid'}                 ),
        ('mpout',  'mpout',  'search manufacturer part',  '/manufacturer_parts/search?',       {'mpid': 'mpid'}                 ),
        ('splk',   'splk',   'link supplier part',        '/manufacturer_part_links/select/?', {'mpid': 'mpid'}                 ),
        ('mpqty',  'mpqty',  '',                          '',                                  None                             ),
        ('sporg',  'sporg',  'supplier organization',     '/organizations/#',                  'spoid'                          ),
        ('spn',    'spn',    'supplier part',             '/supplier_parts/#',                 'spid'                           ),
        ('spdesc', 'spdesc', '',                          '',                                  None                             ),
        ('spunlk', 'spunlk', 'unlink supplier part',      '/manufacturer_part_links/break/?',  {'mpid': 'mpid', 'spid': 'spid'} ),
        ('spedit',  'spedit',  'edit supplier part',      '/supplier_parts/edit?',             {'spid': 'spid'}                 ),
        ('spout',   'spout',   'search supplier part',    '/supplier_parts/search?',           {'spid': 'spid'}                 )
    )
}

manufacturer_part_links_table = {

    'head': (
        ('Cat', 'spcat', 1),
        ('Organization', 'sporg', 1),
        ('Part Number', 'spn',  1),
        ('Description', 'spdesc', 1),
        ('Manufacturer', 'mp', (
            ('Name', 'mporg', 1),
            ('Part Number', 'mpn', 1),
            ('Description', 'mpdesc', 1),
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
        'mpid':     '?mpid',
        'spid':     (0, 'id'),
        'spoid':    (0, 'organization__id'),
        'sporg':    (0, 'organization__name'),
        'spn':      (0, 'part_number'),
        'spcatid':  (0, 'category__id'),
        'spcat':    (0, 'category__name'),
        'spdesc':   (0, 'description'),
        'mporg':    (0, 'manufacturer_part__organization__name'),
        'mpn':      (0, 'manufacturer_part__part_number'),
        'mpdesc':   (0, 'manufacturer_part__description')
    },

    'body': (
        ('spcat',   'spcat',  '', '', None),
        ('sporg',   'sporg',  '', '', None),
        ('spn',     'spn',
            'create link to this part',
            '/manufacturer_part_links/create/?',
            {'mpid': 'mpid', 'spid': 'spid'}
        ),
        ('spdesc',  'spdesc', '', '', None),
        ('mporg',   'mporg',  '', '', None),
        ('mpn',     'mpn',    '', '', None),
        ('mpdesc',  'mpdesc', '', '', None),
    )
}