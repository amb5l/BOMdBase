from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import ManufacturerPart
from .tables import manufacturer_parts_table, manufacturer_part_links_table
from .forms import ManufacturerPartEditForm, ManufacturerPartConfirmForm, \
    ManufacturerPartLinkCreateForm, ManufacturerPartLinkBreakForm

from main.shared import navbar1
from main.flextable import flextable
from main.utils import errmsg, done

from supplier_parts.models import SupplierPart
from supplier_parts.forms import SupplierPartConfirmForm

def manufacturer_parts(request):
    table = flextable(
        request.GET,
        manufacturer_parts_table,
        ManufacturerPart.objects.all() \
            .select_related('organization', 'category', 'unit') \
            .prefetch_related('supplier_parts') \
            .all()
    )
    context = { \
        'title': 'Manufacturer Parts',
        'navbar1': navbar1,
        'navbar2': [
            ('categories', '/part_categories'),
            ('units', '/part_units'),
            ('create new part', 'edit?new')
        ],
        'table': table,
        }
    return render(request, 'base.html', context)

def manufacturer_parts_edit(request):
    if request.method == 'POST':
        form = ManufacturerPartEditForm(request.POST)
        if form.is_valid():
            mp = form.cleaned_data['mp']
            if mp:
                mp.organization = form.cleaned_data['mporg']
                mp.part_number = form.cleaned_data['mpn']
                mp.category = form.cleaned_data['mpcat']
                mp.description = form.cleaned_data['mpdesc']
                mp.unit = form.cleaned_data['mpunit']
                title = 'Manufacturer Parts - Edit'
                notes = 'Manufacturer part <b>' + str(mp) + '</b> edited OK'
            else:
                mp = ManufacturerPart(
                    organization = form.cleaned_data['mporg'],
                    part_number = form.cleaned_data['mpn'],
                    category = form.cleaned_data['mpcat'],
                    description = form.cleaned_data['mpdesc'],
                    unit = form.cleaned_data['mpunit']
                )
                title = 'Manufacturer Parts - New'
                notes = 'Manufacturer part <b>' + str(mp) + '</b> created OK'
            mp.save()
            return done(request, title, notes, 2)
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'new' in request.GET:
            form = ManufacturerPartEditForm()
            title = 'Manufacturer Parts - New'
        else:
            if 'mpid' not in request.GET:
                return errmsg(request, 'Manufacturer Part ID must be specified')
            if ManufacturerPart.objects.filter(id=request.GET.get('mpid')).count() != 1:
                return errmsg(request, 'Manufacturer Part not found in database')
            mp = ManufacturerPart.objects.get(id=request.GET.get('mpid'))
            form = ManufacturerPartEditForm( \
                initial={
                    'mp': mp,
                    'mporg': mp.organization,
                    'mpn': mp.part_number,
                    'mpcat': mp.category,
                    'mpdesc': mp.description,
                    'mpunit': mp.unit
                }
            )
            title = 'Manufacturer Parts - Edit'
        context = { \
            'title': title,
            'navbar1': navbar1,
            'form': form,
            'form_action': '/manufacturer_parts/edit/'
            }
        return render(request, 'base.html', context)

def manufacturer_parts_delete(request):
    if request.method == 'POST':
        form = ManufacturerPartConfirmForm(request.POST)
        if form.is_valid():
            try:
                mp = form.cleaned_data['mp']
                notes = 'Manufacturer part <b>' + str(mp) + '</b> deleted OK'
                mp.delete()
                return done(request, 'Manufacturer Parts - Delete', notes, 2)
            except:
                return errmsg(request, 'Failed to delete manufacturer part (may be in use)')
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'mpid' not in request.GET:
            return errmsg(request, 'Manufacturer Part ID must be specified')
        if ManufacturerPart.objects.filter(id=request.GET.get('mpid')).count() != 1:
            return errmsg(request, 'Manufacturer Part not found in database')
        mp = ManufacturerPart.objects.get(id=request.GET.get('mpid'))
        form = ManufacturerPartConfirmForm( \
            initial={
                'mp': mp,
                'mporg': mp.organization,
                'mpn': mp.part_number,
                'mpcat': mp.category,
                'mpdesc': mp.description,
                'mpunit': mp.unit
            }
        )
        context = { \
            'title': 'Manufacturer Parts - Delete',
            'navbar1': navbar1,
            'form': form,
            'form_action': '/manufacturer_parts/delete/'
            }
        return render(request, 'base.html', context)

def manufacturer_parts_search(request):
    if 'mpid' not in request.GET:
        return errmsg(request, 'Manufacturer Part ID must be specified')
    if request.GET.get('mpid') == 'None':
        return errmsg(request, 'Manufacturer Part does not exist')
    if ManufacturerPart.objects.filter(id=request.GET.get('mpid')).count():
        o = ManufacturerPart.objects.get(id=request.GET.get('mpid'))
        return HttpResponseRedirect(
            'https://www.google.com/search?q=' + \
                o.organization.name + '+' + o.part_number
        )
    else:
        return errmsg(request, 'Part not found in database')

def manufacturer_part_links_select(request):
    if 'mpid' not in request.GET:
        return errmsg(request, 'Manufacturer Part ID must be specified')
    if ManufacturerPart.objects.filter(id=request.GET.get('mpid')).count() != 1:
        return errmsg(request, 'Manufacturer Part not found in database')
    mp = ManufacturerPart.objects.get(id=request.GET.get('mpid'))
    qs = SupplierPart.objects.all() \
        .select_related('organization', 'category') \
        .all()
    if qs.count() == 0:
        return errmsg(request, 'No Supplier Parts exist in database')
    table = flextable(request.GET, manufacturer_part_links_table, qs)
    context = {
        'title': 'Manufacturer Part Links - Select',
        'navbar1': navbar1,
        'heading': 'Manufacturer Part: ' + str(mp),
        'notes': 'Select a Supplier Part to link with this manufacturer part:',
        'table': table
    }
    return render(request, 'base.html', context)

def manufacturer_part_links_create(request):
    if request.method == 'POST':
        form = ManufacturerPartLinkCreateForm(request.POST)
        if form.is_valid():
            try:
                sp = form.cleaned_data['sp']
                mp = form.cleaned_data['mp']
                sp.manufacturer_part = mp
                sp.manufacturer_part_qty = form.cleaned_data['spmpqty']
                sp.save()
                return done(
                    request,
                    'Manufacturer Part Links - Create',
                    'Manufacturer part <b>' + str(mp) + \
                        '</b> now linked to supplier part <b>' + str(sp) + '</b>',
                    3
                )
            except:
                return errmsg(request, 'Failed to link parts')
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'mpid' not in request.GET:
            return errmsg(request, 'Manufacturer Part ID must be specified')
        if ManufacturerPart.objects.filter(id=request.GET.get('mpid')).count() != 1:
            return errmsg(request, 'Manufacturer Part not found in database')
        mp = ManufacturerPart.objects.get(id=request.GET.get('mpid'))
        if 'spid' not in request.GET:
            return errmsg(request, 'Supplier Part ID must be specified')
        if SupplierPart.objects.filter(id=request.GET.get('spid')).count() != 1:
            return errmsg(request, 'Supplier Part not found in database')
        sp = SupplierPart.objects.get(id=request.GET.get('spid'))
        form = ManufacturerPartLinkCreateForm(
            initial={
                'mp': mp,
                'sp': sp,
                'spmp': mp,
                'spmpqty': 1,
                'sporg': sp.organization,
                'spn': sp.part_number,
                'spcat': sp.category,
                'spdesc': sp.description
            }
        )
        notes = ''
        if sp.manufacturer_part:
            notes = '<b>Warning: </b>supplier part <b>' + str(sp) + '</b> ' \
                'is currently linked to manufacturer part <b>' + \
                    str(sp.manufacturer_part) + '</b>.<br>'
        notes += 'Please check and amend Manufacturer Part Quantity if required.'
        context = { \
            'title': 'Manufacturer Part Links - Create',
            'navbar1': navbar1,
            'notes': notes,
            'form': form,
            'form_action': '/manufacturer_part_links/create/'
            }
        return render(request, 'base.html', context)

def manufacturer_part_links_break(request):
    if request.method == 'POST':
        form = ManufacturerPartLinkBreakForm(request.POST)
        if form.is_valid():
            try:
                sp = form.cleaned_data['sp']
                mp = form.cleaned_data['mp']
                sp.manufacturer_part = None
                sp.manufacturer_part_qty = 1
                sp.save()
            except:
                return errmsg(request, 'Failed to break link')
        else:
            print(form.errors) # todo: improve
        return done(
            request,
            'Manufacturer Part Links - Break',
            'Supplier part <b>' + str(sp) + '</b> is no longer linked to ' \
                'manufacturer part <b>' + str(mp) + '</b>',
            2
        )
    else:
        if 'mpid' not in request.GET:
            return errmsg(request, 'Manufacturer Part ID must be specified')
        if ManufacturerPart.objects.filter(id=request.GET.get('mpid')).count() != 1:
            return errmsg(request, 'Manufacturer Part not found in database')
        mp = ManufacturerPart.objects.get(id=request.GET.get('mpid'))
        if 'spid' not in request.GET:
            return errmsg(request, 'Supplier Part ID must be specified')
        if SupplierPart.objects.filter(id=request.GET.get('spid')).count() != 1:
            return errmsg(request, 'Supplier Part not found in database')
        sp = SupplierPart.objects.get(id=request.GET.get('spid'))
        if sp.manufacturer_part != mp:
            return errmsg(request, 'No link exists to break')
        form = ManufacturerPartLinkBreakForm( \
            initial={
                'mp': mp,
                'sp': sp,
                'sporg': sp.organization,
                'spn': sp.part_number,
                'spcat': sp.category,
                'spdesc': sp.description,
                'spmp': sp.manufacturer_part,
                'spmpqty': sp.manufacturer_part_qty
            }
        )
        context = { \
            'title': 'Manufacturer Part Links - Break',
            'navbar1': navbar1,
            'form': form,
            'form_action': '/manufacturer_part_links/break/'
            }
        return render(request, 'base.html', context)