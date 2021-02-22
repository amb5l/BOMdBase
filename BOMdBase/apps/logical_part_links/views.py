from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import LogicalPart2ManufacturerPart
from .tables import logical_part_links_table
from .forms import LogicalPart2ManufacturerPartForm

from logical_parts.models import LogicalPart
from manufacturer_parts.models import ManufacturerPart

from main.utils import done, errmsg
from main.shared import navbar1
from main.flextable import flextable

def logical_part_links_select(request):
    if 'lpid' not in request.GET:
        return errmsg(request, 'Logical Part ID must be specified')
    print(request.GET.get('lpid'))
    if LogicalPart.objects.filter(id=request.GET.get('lpid')).count() != 1:
        return errmsg(request, 'Logical Part not found in database')
    lp = LogicalPart.objects.get(id=request.GET.get('lpid'))
    qs = ManufacturerPart.objects.all() \
        .select_related('organization', 'category', 'unit') \
        .prefetch_related('supplier_parts') \
        .all()
    if qs.count() == 0:
        return errmsg(request, 'No Manufacturer Parts exist in database')
    table = flextable(request.GET, logical_part_links_table, qs)
    context = {
        'title': 'Logical Part - Select Manufacturer Part',
        'navbar1': navbar1,
        'heading': 'Logical Part: ' + lp.part_number,
        'notes': 'Select a Manufacturer Part to link:',
        'table': table
    }
    return render(request, 'base.html', context)

def logical_part_links_create(request):
    if request.method == 'POST':
        form = LogicalPart2ManufacturerPartForm(request.POST)
        if form.is_valid():
            try:
                LogicalPart2ManufacturerPart.objects.update_or_create(
                    logical_part=form.cleaned_data['lp'],
                    manufacturer_part=form.cleaned_data['mp']
                )
            except:
                return errmsg(request, 'Failed to create link')
        else:
            print(form.errors) # todo: improve
        return done(
            request, 'Logical Part Link Created',
            'Logical part <b>' + str(form.cleaned_data['lp']) + \
                '</b> now linked to manufacturer part <b>' + \
                str(form.cleaned_data['mp']) + '</b>',
            3
        )
    else:
        if 'lpid' not in request.GET:
            return errmsg(request, 'Logical Part ID must be specified')
        if LogicalPart.objects.filter(id=request.GET.get('lpid')).count() != 1:
            return errmsg(request, 'Logical Part not found in database')
        lp = LogicalPart.objects.get(id=request.GET.get('lpid'))
        if 'mpid' not in request.GET:
            return errmsg(request, 'Manufacturer Part ID must be specified')
        if ManufacturerPart.objects.filter(id=request.GET.get('mpid')).count() != 1:
            return errmsg(request, 'Manufacturer Part not found in database')
        mp = ManufacturerPart.objects.get(id=request.GET.get('mpid'))
        if LogicalPart2ManufacturerPart.objects.filter(
            logical_part=lp, manufacturer_part=mp
        ).count():
            return errmsg(request, 'Parts are already linked')
        note = lp.notes.note if lp.notes else ''
        form = LogicalPart2ManufacturerPartForm( \
            initial={
                'lp': lp,
                'lpn': lp.part_number,
                'lpdesc': lp.description,
                'lpcat': lp.category,
                'lpnotes': note,
                'mp': mp,
                'mporg': mp.organization,
                'mpn': mp.part_number,
                'mpcat': mp.category,
                'mpdesc': mp.description,
                'mpunit': mp.unit
            }
        )
        context = { \
            'title': 'Logical Part - Create Manufacturer Part Link',
            'navbar1': navbar1,
            'form': form,
            'form_action': '/logical_part_links/create/'
            }
        return render(request, 'base.html', context)

def logical_part_links_break(request):
    if request.method == 'POST':
        form = LogicalPart2ManufacturerPartForm(request.POST)
        if form.is_valid():
            try:
                lp=form.cleaned_data['lp']
                mp=form.cleaned_data['mp']
                LogicalPart2ManufacturerPart.objects.filter(
                    logical_part=lp,
                    manufacturer_part=mp
                ).delete()
            except:
                return errmsg(request, 'Failed to break link')
        else:
            print(form.errors) # todo: improve
        return done(
            request, 'Logical Part Link Broken',
            'Logical part <b>' + str(form.cleaned_data['lp']) + \
                '</b> unlinked from manufacturer part <b>' + \
                str(form.cleaned_data['mp']) + '</b>',
            2
        )
    else:
        if 'lpid' not in request.GET:
            return errmsg(request, 'Logical Part ID must be specified')
        if LogicalPart.objects.filter(id=request.GET.get('lpid')).count() != 1:
            return errmsg(request, 'Logical Part not found in database')
        lp = LogicalPart.objects.get(id=request.GET.get('lpid'))
        if 'mpid' not in request.GET:
            return errmsg(request, 'Manufacturer Part ID must be specified')
        if ManufacturerPart.objects.filter(id=request.GET.get('mpid')).count() != 1:
            return errmsg(request, 'Manufacturer Part not found in database')
        mp = ManufacturerPart.objects.get(id=request.GET.get('mpid'))
        if LogicalPart2ManufacturerPart.objects.filter(
            logical_part=lp, manufacturer_part=mp
        ).count() == 0:
            return errmsg(request, 'No part link exists to be broken')
        # todo: catch errors
        note = lp.notes.note if lp.notes else ''
        form = LogicalPart2ManufacturerPartForm( \
            initial={
                'lp': lp,
                'lpn': lp.part_number,
                'lpdesc': lp.description,
                'lpcat': lp.category,
                'lpnotes': note,
                'mp': mp,
                'mporg': mp.organization,
                'mpn': mp.part_number,
                'mpcat': mp.category,
                'mpdesc': mp.description,
                'mpunit': mp.unit
            }
        )
        context = { \
            'title': 'Logical Part - Break Manufacturer Part Link',
            'navbar1': navbar1,
            'form': form,
            'form_action': '/logical_part_links/break/'
            }
        return render(request, 'base.html', context)