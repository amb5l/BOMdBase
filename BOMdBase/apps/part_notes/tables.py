from main.utils import icon

part_notes_table = {

    'head': (
        ('Note', 'note', 1),
        ('', 'edit', 1),
        ('', 'del', 1)
    ),

    'sort': {'note': 'note'},

    'hide': {},

    'aliases': {
        'id':       (0, 'id'),
        'note':     (0, 'note'),
        'edit':     icon('edit'),
        'del':      icon('delete')
    },

    'body': (
        ('note',  'note', '',                '',        None           ),
        ('edit',  'edit', 'edit category',   'edit?',   {'pnid': 'id'} ),
        ('del',   'del',  'delete category', 'delete?', {'pnid': 'id'} )
    )

}