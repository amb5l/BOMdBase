from django.shortcuts import render

from .shared import navbar1

def main(request):
    notes = 'Hello!'
    context = { \
        'navbar1': navbar1,
        'navbar2': [
            ('Backup/Export', '/backup'),
            ('Restore/Import', '/restore'),
            ('Admin', '/admin')
        ],
        'notes': notes
        }
    return render(request, 'base.html', context)