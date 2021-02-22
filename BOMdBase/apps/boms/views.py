from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import BOM, BOMItem
from .tables import boms_table, boms_interactive_table, boms_printable_table
from .forms import BOMEditForm, BOMConfirmForm, BOMImportForm
from .bom_import_orcad import bom_import_orcad
from .bom_export_csv import bom_export_csv

from main.shared import navbar1
from main.flextable import flextable
from main.utils import errmsg, done

def boms(request):
    table = flextable(
        request.GET,
        boms_table,
        BOM.objects.all()
    )
    context = { \
        'title': 'BOMs',
        'navbar1': navbar1,
        'navbar2': [
            ('create new BOM', 'edit?new'),
            ('import BOM', 'import')
        ],
        'table': table,
        }
    return render(request, 'base.html', context)

def boms_edit(request):
    if request.method == 'POST':
        form = BOMEditForm(request.POST)
        if form.is_valid():
            bom = form.cleaned_data['bom']
            if bom:
                bom.name = form.cleaned_data['bomname']
                bom.description = form.cleaned_data['bomdesc']
                title = 'BOMs - Edit'
                notes = 'BOM <b>' + str(bom) + '</b> edited OK'
            else:
                bom = BOM(
                    name = form.cleaned_data['bomname'],
                    description = form.cleaned_data['bomdesc']
                )
                title = 'BOMs - New'
                notes = 'BOM <b>' + str(bom) + '</b> created OK'
            bom.save()
            return done(request, title, notes, 2)
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'new' in request.GET:
            form = BOMEditForm()
            title = 'BOMs - New'
        else:
            if 'bomid' not in request.GET:
                return errmsg(request, 'BOM ID must be specified')
            if BOM.objects.filter(id=request.GET.get('bomid')).count() != 1:
                return errmsg(request, 'BOM not found in database')
            bom = BOM.objects.get(id=request.GET.get('bomid'))
            form = BOMEditForm( \
                initial={
                    'bom': bom,
                    'bomname': bom.name,
                    'bomdesc': bom.description
                }
            )
            title = 'BOMs - Edit'
        context = { \
            'title': title,
            'navbar1': navbar1,
            'form': form,
            'form_action': '/boms/edit/'
            }
        return render(request, 'base.html', context)

def boms_delete(request):
    if request.method == 'POST':
        form = BOMConfirmForm(request.POST)
        if form.is_valid():
            try:
                bom = form.cleaned_data['bom']
                notes = 'BOM <b>' + str(bom) + '</b> deleted OK'
                bom.delete()
                return done(request, 'BOMs - Delete', notes, 2)
            except:
                return errmsg(request, 'Failed to delete BOM')
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'bomid' not in request.GET:
            return errmsg(request, 'BOM ID must be specified')
        if BOM.objects.filter(id=request.GET.get('bomid')).count() != 1:
            return errmsg(request, 'BOM not found in database')
        bom = BOM.objects.get(id=request.GET.get('bomid'))
        form = BOMConfirmForm( \
            initial={
                'bom': bom,
                'bomname': bom.name,
                'bomdesc': bom.description
            }
        )
        context = { \
            'title': 'BOMs - Delete',
            'navbar1': navbar1,
            'form': form,
            'form_action': '/boms/delete/'
            }
        return render(request, 'base.html', context)

def boms_interactive(request):
    if 'bomid' not in request.GET:
        return errmsg(request, 'BOM ID must be specified')
    bomid = request.GET.get('bomid')
    if BOM.objects.filter(id=bomid).count() != 1:
        return errmsg(request, 'BOM not found in database')
    bom = BOM.objects.get(id=bomid)
    qs = BOMItem.objects.filter(bom=bomid).all() \
        .select_related('logical_part') \
        .prefetch_related(
            'logical_part__manufacturer_parts',
            'logical_part__manufacturer_parts__manufacturer_part__supplier_parts'
        )
    if qs.count() == 0:
        return errmsg(request, 'No BOM items found in database')
    table = flextable(request.GET, boms_interactive_table, qs)
    context = {
        'title': bom.name,
        'notes': bom.description,
        'navbar1': navbar1,
        'navbar2': [
            ('printable', '/boms/printable/?' + request.GET.urlencode()),
            ('export', '/boms/export/?' + request.GET.urlencode())
        ],
        'table': table,
        }
    return render(request, 'base.html', context)

def boms_printable(request):
    if 'bomid' not in request.GET:
        return errmsg(request, 'BOM ID must be specified')
    bomid = request.GET.get('bomid')
    if BOM.objects.filter(id=bomid).count() != 1:
        return errmsg(request, 'BOM not found in database')
    bom = BOM.objects.get(id=bomid)
    qs = BOMItem.objects.filter(bom=request.GET.get('bomid')).all() \
        .select_related('logical_part') \
        .prefetch_related(
            'logical_part__manufacturer_parts',
            'logical_part__manufacturer_parts__manufacturer_part__supplier_parts'
        )
    if qs.count() == 0:
        return errmsg(request, 'No BOM items found in database')
    table = flextable(request.GET, boms_printable_table, qs)
    context = {
        'title': bom.name,
        'notes': bom.description,
        'table': table,
        }
    return render(request, 'base.html', context)

def boms_import(request):
    if request.method == 'POST':
        form = BOMImportForm(request.POST, request.FILES)
        if form.is_valid():
            log = bom_import_orcad(
                    form.cleaned_data['name'],
                    request.FILES['file'],
                    form.cleaned_data['create_parts'],
                    form.cleaned_data['dry_run']
                )
            return done(request, 'BOM Import (OrCAD)', log, 1)
    else:
        form = BOMImportForm()
    context = { \
        'title': 'BOM Import (OrCAD)',
        'navbar1': navbar1,
        'form': form,
        'form_action': '/boms/import/'
        }
    return render(request, 'base.html', context)

def boms_export(request):
    return bom_export_csv(request, boms_interactive_table['sort'])