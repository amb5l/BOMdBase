from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import SupplierPart
from .tables import supplier_parts_table, supplier_part_link_table
from .forms import SupplierPartEditForm, SupplierPartConfirmForm, \
    SupplierPartLinkCreateForm, SupplierPartLinkBreakForm

from manufacturer_parts.models import ManufacturerPart

from main.shared import navbar1
from main.flextable import flextable
from main.utils import errmsg, done

def supplier_parts(request):
    table = flextable(
        request.GET,
        supplier_parts_table,
        SupplierPart.objects.all()
            .select_related('organization', 'category', 'manufacturer_part')
            .all()
    )
    context = { \
        'title': 'Supplier Parts',
        'navbar1': navbar1,
        'navbar2': [
            ('categories', '/part_categories'),
            ('create new part', 'edit?new')
        ],
        'table': table,
        }
    return render(request, 'base.html', context)

def supplier_parts_edit(request):
    if request.method == 'POST':
        form = SupplierPartEditForm(request.POST)
        if form.is_valid():
            sp = form.cleaned_data['sp']
            if sp:
                sp.organization = form.cleaned_data['sporg']
                sp.part_number = form.cleaned_data['spn']
                sp.category = form.cleaned_data['spcat']
                sp.description = form.cleaned_data['spdesc']
                sp.manufacturer_part = form.cleaned_data['spmp']
                sp.manufacturer_part_qty = form.cleaned_data['spmpqty']
                title = 'Supplier Parts - Edit'
                notes = 'Supplier part <b>' + str(sp) + '</b> edited OK'
            else:
                sp = SupplierPart(
                    organization = form.cleaned_data['sporg'],
                    part_number = form.cleaned_data['spn'],
                    category = form.cleaned_data['spcat'],
                    description = form.cleaned_data['spdesc'],
                    manufacturer_part = form.cleaned_data['spmp'],
                    manufacturer_part_qty = form.cleaned_data['spmpqty']
                )
                title = 'Supplier Parts - New'
                notes = 'Supplier part <b>' + str(sp) + '</b> created OK'
            sp.save()
            return done(request, title, notes, 2)
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'new' in request.GET:
            form = SupplierPartEditForm()
            title = 'Supplier Parts - New'
        else:
            if 'spid' not in request.GET:
                return errmsg(request, 'Supplier Part ID must be specified')
            if SupplierPart.objects.filter(id=request.GET.get('spid')).count() != 1:
                return errmsg(request, 'Supplier Part not found in database')
            sp = SupplierPart.objects.get(id=request.GET.get('spid'))
            form = SupplierPartEditForm( \
                initial={
                    'sp': sp,
                    'sporg': sp.organization,
                    'spn': sp.part_number,
                    'spcat': sp.category,
                    'spdesc': sp.description,
                    'spmp': sp.manufacturer_part,
                    'spmpqty': sp.manufacturer_part_qty
                }
            )
            title = 'Supplier Parts - Edit'
        context = { \
            'title': title,
            'navbar1': navbar1,
            'form': form,
            'form_action': '/supplier_parts/edit/'
            }
        return render(request, 'base.html', context)

def supplier_parts_delete(request):
    if request.method == 'POST':
        form = SupplierPartConfirmForm(request.POST)
        if form.is_valid():
            try:
                sp = form.cleaned_data['sp']
                notes = 'Supplier part <b>' + str(sp) + '</b> deleted OK'
                sp.delete()
                return done(request, 'Supplier Parts - Delete', notes, 2)
            except:
                return errmsg(request, 'Failed to delete supplier part (may be in use)')
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'spid' not in request.GET:
            return errmsg(request, 'Supplier Part ID must be specified')
        if SupplierPart.objects.filter(id=request.GET.get('spid')).count() != 1:
            return errmsg(request, 'Supplier Part not found in database')
        sp = SupplierPart.objects.get(id=request.GET.get('spid'))
        form = SupplierPartConfirmForm( \
            initial={
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
            'title': 'Supplier Parts - Delete',
            'navbar1': navbar1,
            'form': form,
            'form_action': '/supplier_parts/delete/'
            }
        return render(request, 'base.html', context)

def supplier_parts_search(request):
    if 'spid' not in request.GET:
        return errmsg(request, 'Supplier Part ID must be specified')
    if request.GET.get('spid') == 'None':
        return errmsg(request, 'Supplier Part does not exist')
    if SupplierPart.objects.filter(id=request.GET.get('spid')).count():
        o = SupplierPart.objects.get(id=request.GET.get('spid'))
        return HttpResponseRedirect(
            'https://www.google.com/search?q=' + \
                o.organization.name + '+' + o.part_number
        )
    else:
        return errmsg(request, 'Part not found in database')

def supplier_part_link_select(request):
    if 'spid' not in request.GET:
        return errmsg(request, 'Supplier Part ID must be specified')
    if SupplierPart.objects.filter(id=request.GET.get('spid')).count() != 1:
        return errmsg(request, 'Supplier Part not found in database')
    sp = SupplierPart.objects.get(id=request.GET.get('spid'))
    qs = ManufacturerPart.objects.all() \
        .select_related('organization', 'category', 'unit') \
        .prefetch_related('supplier_parts') \
        .all()
    if qs.count() == 0:
        return errmsg(request, 'No Supplier Parts exist in database')
    table = flextable(request.GET, supplier_part_link_table, qs)
    context = {
        'title': 'Supplier Part Link - Select',
        'navbar1': navbar1,
        'heading': 'Supplier Part: ' + str(sp),
        'notes': 'Select a Manufacturer Part to link with this supplier part:',
        'table': table
    }
    return render(request, 'base.html', context)

def supplier_part_link_create(request):
    if request.method == 'POST':
        form = SupplierPartLinkCreateForm(request.POST)
        if form.is_valid():
            try:
                sp = form.cleaned_data['sp']
                mp = form.cleaned_data['mp']
                sp.manufacturer_part = mp
                sp.manufacturer_part_qty = form.cleaned_data['spmpqty']
                sp.save()
                return done(
                    request,
                    'Supplier Part Link - Create',
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
        form = SupplierPartLinkCreateForm(
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
            'title': 'Supplier Part Link - Create',
            'navbar1': navbar1,
            'notes': notes,
            'form': form,
            'form_action': '/supplier_part_link/create/'
            }
        return render(request, 'base.html', context)

def supplier_part_link_break(request):
    if request.method == 'POST':
        form = SupplierPartLinkBreakForm(request.POST)
        if form.is_valid():
            try:
                sp = form.cleaned_data['sp']
                mp = sp.manufacturer_part
                sp.manufacturer_part = None
                sp.manufacturer_part_qty = 1
                sp.save()
            except:
                return errmsg(request, 'Failed to break link')
        else:
            print(form.errors) # todo: improve
        return done(
            request,
            'Supplier Part Link - Break',
            'Supplier part <b>' + str(sp) + '</b> is no longer linked to ' \
                'manufacturer part <b>' + str(mp) + '</b>',
            2
        )
    else:
        if 'spid' not in request.GET:
            return errmsg(request, 'Supplier Part ID must be specified')
        if SupplierPart.objects.filter(id=request.GET.get('spid')).count() != 1:
            return errmsg(request, 'Supplier Part not found in database')
        sp = SupplierPart.objects.get(id=request.GET.get('spid'))
        if not sp.manufacturer_part:
            return errmsg(request, 'No manufacturer part link exists to break')
        form = SupplierPartLinkBreakForm( \
            initial={
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
            'title': 'Supplier Part Link - Break',
            'navbar1': navbar1,
            'form': form,
            'form_action': '/supplier_part_link/break/'
            }
        return render(request, 'base.html', context)