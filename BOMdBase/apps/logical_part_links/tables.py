from main.utils import icon

logical_part_links_table = {

    'head': (
        ('Cat', 'mpcat', 1),
        ('Organization', 'mporg', 1),
        ('Part Number', 'mpn',  1),
        ('Description', 'mpdesc', 1),
        ('Unit', 'mpunit', 1),
        ('Supplier', 'sp', (
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

    'relations': ('supplier_parts', ),

    'aliases': {
        'lpid':     '?lpid',
        'mpid':     (0, 'id'),
        'mpoid':    (0, 'organization__id'),
        'mporg':    (0, 'organization__name'),
        'mpn':      (0, 'part_number'),
        'mpcatid':  (0, 'category__id'),
        'mpcat':    (0, 'category__name'),
        'mpdesc':   (0, 'description'),
        'mpuid':    (0, 'unit__id'),
        'mpunit':   (0, 'unit__name'),
        'spid':     (1, 'id'),
        'spoid':    (1, 'organization__id'),
        'sporg':    (1, 'organization__name'),
        'spn':      (1, 'part_number'),
        'spdesc':   (1, 'description')
    },

    'body': (
        ('mpcat',  'mpcat',  '', '', None ),
        ('mporg',  'mporg',  '', '', None ),
        ('mpn',    'mpn',
            'create link to this part',
            '/logical_part_links/create/?',
            {'lpid': 'lpid', 'mpid': 'mpid'}
        ),
        ('mpdesc', 'mpdesc', '', '', None ),
        ('mpunit', 'mpunit', '', '', None ),
        ('sporg',  'sporg',  '', '', None ),
        ('spn',    'spn',    '', '', None ),
        ('spdesc', 'spdesc', '', '', None )
    )
}