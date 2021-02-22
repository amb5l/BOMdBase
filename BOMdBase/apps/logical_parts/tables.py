from main.utils import icon

logical_parts_table = {

    'head': (
        ('Cat', 'lpcat', 1),
        ('Part Number', 'lpn',  1),
        ('Description', 'lpdesc', 1),
        ('Notes', 'lpnotes', 1),
        ('', 'lpedit', 1),
        ('', 'lpdel', 1),
        ('Manufacturer', 'mp', (
            ('', 'mplk', 1),
            ('Name', 'mporg', 1),
            ('Part', 'mpn', 1),
            ('Description', 'mpdesc', 1),
            ('', 'mpedit', 1),
            ('', 'mpunlk', 1),
            ('', 'mpout', 1)
        )),
        ('Supplier', 'sp', (
            ('', 'splk', 1),
            ('Name', 'sporg', 1),
            ('Part', 'spn', 1),
            ('Description', 'spdesc', 1),
            ('', 'spedit', 1),
            ('', 'spunlk', 1),
            ('', 'spout', 1)
        ))
    ),

    'sort': {
        'lpcat': 'category__name',
        'lpn': 'part_number',
        'lpdesc': 'description',
        'lpnotes': 'notes__note'
    },

    'hide': {
        'lpcat': 'Category',
        'lpdesc': 'Description',
        'lpnotes': 'Notes',
        'mp': 'Manufacturer Parts',
        'mpdesc': 'Manufacturer Part Descriptions',
        'sp': 'Supplier Parts',
        'spdesc': 'Supplier Part Descriptions',
    },

    'relations': (
        'manufacturer_parts',   # level 1: LogicalPart2ManufacturerPart (1:n)
        'manufacturer_part',    # level 2: ManufacturerPart (1:1)
        'supplier_parts'        # level 3: SupplierPart (1:n)
    ),

    'aliases': {
        'lpid':     (0, 'id'),
        'lpcat':    (0, 'category__name'),
        'lpn':      (0, 'part_number'),
        'lpdesc':   (0, 'description'),
        'lpnotes':  (0, 'notes__note'),
        'lpedit':   icon('edit'),
        'lpdel':    icon('delete'),
        'mpid':     (2, 'id'),
        'mpoid':    (2, 'organization__id'),
        'mporg':    (2, 'organization__name'),
        'mpn':      (2, 'part_number'),
        'mpdesc':   (2, 'description'),
        'mplk':     icon('link+'),
        'mpunlk':   (2, '#' + icon('unlink')),
        'mpedit':   (2, '#' + icon('edit')),
        'mpout':    (2, '#' + icon('extlink')),
        'spid':     (3, 'id'),
        'spoid':    (3, 'organization__id'),
        'sporg':    (3, 'organization__name'),
        'spn':      (3, 'part_number'),
        'spdesc':   (3, 'description'),
        'splk':     (2, '#' + icon('link+')),
        'spout':    (3, '#' + icon('extlink')),
        'spedit':   (3, '#' + icon('edit')),
        'spunlk':   (3, '#' + icon('unlink'))
    },

    'body': (
        ('lpcat',   'lpcat',   '',                           '',                                  None                             ),
        ('lpn',     'lpn',     '',                           '',                                  None                             ),
        ('lpdesc',  'lpdesc',  '',                           '',                                  None                             ),
        ('lpnotes', 'lpnotes', '',                           '',                                  None                             ),
        ('lpedit',  'lpedit',  'edit logical part',          'edit?',                             {'lpid': 'lpid'}                 ),
        ('lpdel',   'lpdel',   'delete logical part',        'delete?',                           {'lpid': 'lpid'}                 ),
        ('mplk',    'mplk',    'link new manufacturer part', '/logical_part_links/select/?',      {'lpid': 'lpid'}                 ),
        ('mporg',   'mporg',   'manufacturer organization',  '/organizations/#',                  'mpoid'                          ),
        ('mpn',     'mpn',     'manufacturer part',          '/manufacturer_parts/#',             'mpid'                           ),
        ('mpdesc',  'mpdesc',  '',                           '',                                  None                             ),
        ('mpunlk',  'mpunlk',  'unlink manufacturer part',   '/logical_part_links/break/?',       {'lpid': 'lpid', 'mpid': 'mpid'} ),
        ('mpedit',  'mpedit',  'edit manufacturer part',     '/manufacturer_parts/edit?',         {'mpid': 'mpid'}                 ),
        ('mpout',   'mpout',   'search manufacturer part',   '/manufacturer_parts/search?',       {'mpid': 'mpid'}                 ),
        ('splk',    'splk',    'link new supplier part',     '/manufacturer_part_links/select/?', {'mpid': 'mpid'}                 ),
        ('sporg',   'sporg',   'supplier organization',      '/organizations#',                   'spoid'                          ),
        ('spn',     'spn',     'supplier part',              '/supplier_parts#',                  'spid'                           ),
        ('spdesc',  'spdesc',  '',                           '',                                  None                             ),
        ('spunlk',  'spunlk',  'unlink supplier part',       '/manufacturer_part_links/break/?', {'mpid': 'mpid', 'spid': 'spid'}  ),
        ('spedit',  'spedit',  'edit supplier part',         'supplier_parts/edit?',             {'spid': 'spid'}                  ),
        ('spout',   'spout',   'search supplier part',       '/supplier_parts/search?',          {'spid': 'spid'}                  )
    )
}