from main.utils import icon

part_units_table = {

    'head': (
        ('Name', 'name', 1),
        ('Description', 'desc', 1),
        ('', 'edit', 1),
        ('', 'del', 1)
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
        ('name',  'name', '',                '',        None           ),
        ('desc',  'desc', '',                '',        None           ),
        ('edit',  'edit', 'edit category',   'edit?',   {'puid': 'id'} ),
        ('del',   'del',  'delete category', 'delete?', {'puid': 'id'} )
    )
}