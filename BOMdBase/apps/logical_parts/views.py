from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import LogicalPart
from .tables import logical_parts_table
from .forms import LogicalPartEditForm
from .forms import LogicalPartConfirmForm

from main.shared import navbar1
from main.flextable import flextable
from main.utils import errmsg, done

def logical_parts(request):
    table = flextable(
        request.GET,
        logical_parts_table,
        LogicalPart.objects.all() \
            .select_related('category')
            .prefetch_related(
                'manufacturer_parts',
                'manufacturer_parts__manufacturer_part__supplier_parts'
            ) \
            .all(),
    )
    context = { \
        'title': 'Logical Parts',
        'navbar1': navbar1,
        'navbar2': [
            ('categories', '/part_categories'),
            ('notes', '/part_notes'),
            ('create new part', 'edit?new')
        ],
        'table': table,
        }
    return render(request, 'base.html', context)

def logical_parts_edit(request):
    if request.method == 'POST':
        form = LogicalPartEditForm(request.POST)
        if form.is_valid():
            lp = form.cleaned_data['lp']
            if lp:
                lp.part_number = form.cleaned_data['lpn']
                lp.category = form.cleaned_data['lpcat']
                lp.description = form.cleaned_data['lpdesc']
                lp.notes = form.cleaned_data['lpnotes']
                title = 'Logical Parts - Edit'
                notes = 'Logical part <b>' + str(lp) + '</b> edited OK'
            else:
                lp = LogicalPart(
                    part_number = form.cleaned_data['lpn'],
                    category = form.cleaned_data['lpcat'],
                    description = form.cleaned_data['lpdesc'],
                    notes = form.cleaned_data['lpnotes']
                )
                title = 'Logical Parts - New'
                notes = 'Logical part <b>' + lp.part_number + '</b>' \
                    ' created OK'
            lp.save()
            return done(request, title, notes, 2)
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'new' in request.GET:
            form = LogicalPartEditForm()
            title = 'Logical Parts - New'
        else:
            if 'lpid' not in request.GET:
                return errmsg(request, 'Logical; Part ID must be specified')
            if LogicalPart.objects.filter(id=request.GET.get('lpid')).count() != 1:
                return errmsg(request, 'Logical Part not found in database')
            lp = LogicalPart.objects.get(id=request.GET.get('lpid'))
            form = LogicalPartEditForm( \
                initial={
                    'lp': lp,
                    'lpn': lp.part_number,
                    'lpcat': lp.category,
                    'lpdesc': lp.description,
                    'lpnotes': lp.notes
                }
            )
            title = 'Logical Parts - Edit'
        context = { \
            'title': title,
            'navbar1': navbar1,
            'form': form,
            'form_action': '/logical_parts/edit/'
            }
        return render(request, 'base.html', context)

def logical_parts_delete(request):
    if request.method == 'POST':
        form = LogicalPartConfirmForm(request.POST)
        if form.is_valid():
            try:
                lp = form.cleaned_data['lp']
                notes = 'Logical part <b>' + str(lp) + '</b> deleted OK'
                lp.delete()
                return done(request, 'Logical Parts - Delete', notes, 2)
            except:
                return errmsg(request, 'Failed to delete logical part (may be in use)')
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'lpid' not in request.GET:
            return errmsg(request, 'Logical Part ID must be specified')
        if LogicalPart.objects.filter(id=request.GET.get('lpid')).count() != 1:
            return errmsg(request, 'Logical Part not found in database')
        lp = LogicalPart.objects.get(id=request.GET.get('lpid'))
        form = LogicalPartConfirmForm( \
            initial={
                'lp': lp,
                'lpn': lp.part_number,
                'lpcat': lp.category,
                'lpdesc': lp.description,
                'lpnotes': lp.notes
            }
        )
        context = { \
            'title': 'Logical Parts - Delete',
            'navbar1': navbar1,
            'form': form,
            'form_action': '/logical_parts/delete/'
            }
        return render(request, 'base.html', context)