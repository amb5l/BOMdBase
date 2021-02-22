from main.utils import icon

organizations_table = {

    'head': (
        ('Name', 'name', 1),
        ('Is Manufacturer', 'mfg', 1),
        ('Is Supplier', 'sup', 1),
        ('URL', 'url', 1),
        ('Notes', 'notes', 1),
        ('', 'edit', 1),
        ('', 'del', 1)
    ),

    'sort': {
        'name': 'name',
        'mfg': 'manufacturer',
        'sup': 'supplier',
        'notes': 'notes'
    },

    'hide': {
        'notes': 'Notes'
    },

    'aliases': {
        'id':    (0, 'id'),
        'name':  (0, 'name'),
        'mfg':   (0, 'manufacturer'),
        'sup':   (0, 'supplier'),
        'url':   (0, 'url'),
        'notes': (0, 'notes'),
        'edit':  icon('edit'),
        'del':   icon('delete')
    },

    'body': (
        ('name',  'name',  '',                '',        None            ),
        ('mfg',   'mfg',   '',                '',        None            ),
        ('sup',   'sup',   '',                '',        None            ),
        ('url',   'url',   '',                '',        None            ),
        ('notes', 'notes', '',                '',        None            ),
        ('edit',  'edit',  'edit category',   'edit?',   {'orgid': 'id'} ),
        ('del',   'del',   'delete category', 'delete?', {'orgid': 'id'} )
    )
}