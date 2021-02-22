from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import PartUnit
from .tables import part_units_table
from .forms import PartUnitEditForm, PartUnitConfirmForm

from main.shared import navbar1
from main.flextable import flextable
from main.utils import errmsg, done

def part_units(request):
    table = flextable(
        request.GET,
        part_units_table,
        PartUnit.objects.all()
    )
    context = { \
        'title': 'Part Units',
        'navbar1': navbar1,
        'navbar2': [
            ('categories', '/part_categories'),
            ('notes', '/part_notes'),
            ('create new unit', 'edit?new')
        ],
        'table': table,
        }
    return render(request, 'base.html', context)

def part_units_edit(request):
    if request.method == 'POST':
        form = PartUnitEditForm(request.POST)
        if form.is_valid():
            pu = form.cleaned_data['pu']
            if pu:
                pu.name = form.cleaned_data['puname']
                pu.description = form.cleaned_data['pudesc']
                title = 'Part Units - Edit'
                notes = 'Part Unit <b>' + str(pu) + '</b> edited OK'
            else:
                pu = PartUnit(
                    name = form.cleaned_data['puname'],
                    description = form.cleaned_data['pudesc']
                )
                title = 'Part Units - New'
                notes = 'Part Unit <b>' + str(pu) + '</b> created OK'
            pu.save()
            return done(request, title, notes, 2)
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'new' in request.GET:
            form = PartUnitEditForm()
            title = 'Part Units - New'
        else:
            if 'puid' not in request.GET:
                return errmsg(request, 'Part Unit ID must be specified')
            if PartUnit.objects.filter(id=request.GET.get('puid')).count() != 1:
                return errmsg(request, 'Part Unit not found in database')
            pu = PartUnit.objects.get(id=request.GET.get('puid'))
            form = PartUnitEditForm( \
                initial={
                    'pu': pu,
                    'puname': pu.name,
                    'pudesc': pu.description
                }
            )
            title = 'Part Units - Edit'
        context = { \
            'title': title,
            'navbar1': navbar1,
            'form': form,
            'form_action': '/part_units/edit/'
            }
        return render(request, 'base.html', context)

def part_units_delete(request):
    if request.method == 'POST':
        form = PartUnitConfirmForm(request.POST)
        if form.is_valid():
            try:
                pu = form.cleaned_data['pu']
                notes = 'Part Unit <b>' + str(pu) + '</b> deleted OK'
                pu.delete()
                return done(request, 'Part Units - Delete', notes, 2)
            except:
                return errmsg(request, 'Failed to delete part unit (may be in use)')
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'puid' not in request.GET:
            return errmsg(request, 'Part Unit ID must be specified')
        if PartUnit.objects.filter(id=request.GET.get('puid')).count() != 1:
            return errmsg(request, 'Part Unit not found in database')
        pu = PartUnit.objects.get(id=request.GET.get('puid'))
        form = PartUnitConfirmForm( \
            initial={
                'pu': pu,
                'puname': pu.name,
                'pudesc': pu.description
            }
        )
        context = { \
            'title': 'Part Units - Delete',
            'navbar1': navbar1,
            'form': form,
            'form_action': '/part_units/delete/'
            }
        return render(request, 'base.html', context)