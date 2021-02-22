from django.shortcuts import render

from .shared import navbar1

def rgetattr(obj, attr_path):
    if obj:
        if type(attr_path) == str:
            attr_path = attr_path.split('__')
        if len(attr_path) == 1:
            return getattr(obj, attr_path[0])
        else:
            return rgetattr(getattr(obj, attr_path[0]), attr_path[1:])
    else:
        return None

def icon(function):
    # cross reference function to Material Design icon
    lookup = {
        'dots':      'more_horiz',
        'up':        'expand_less',
        'down':      'expand_more',
        'updown':    'unfold_more',
        'hide':      'visibility_off',
        'edit':      'create',
        'delete':    'delete_forever',
        'link':      'link',
        'link+':     'add_link',
        'unlink':    'link_off',
        'extlink':   'call_made',
        'checked':   'check_box',
        'unchecked': 'check_box_outline_blank',
        'report':    'list_alt'
    }
    if function in lookup:
        return '<i class="material-icons">' + lookup[function] + '</i>'
    return '?icon?'

def done(request, title, notes=None, resume=None):
    context = { \
        'title': title,
        'navbar1': navbar1,
        'notes': notes,
        'resume': resume
        }
    request.session['refresh'] = 'true'
    return render(request, 'base.html', context)

def errmsg(request, text):
    return render(request, 'base.html', {
        'title': 'Error',
        'notes': text
    })