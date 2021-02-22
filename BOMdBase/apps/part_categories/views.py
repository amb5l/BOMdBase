from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import PartCategory
from .tables import part_categories_table
from .forms import PartCategoryEditForm, PartCategoryConfirmForm

from main.shared import navbar1
from main.flextable import flextable
from main.utils import errmsg, done

def part_categories(request):
    table = flextable(
        request.GET,
        part_categories_table,
        PartCategory.objects.all()
    )
    context = { \
        'title': 'Part Categories',
        'navbar1': navbar1,
        'navbar2': [
            ('notes', '/part_notes'),
            ('units', '/part_units'),
            ('create new category', 'edit?new')
        ],
        'table': table,
        }
    return render(request, 'base.html', context)

def part_categories_edit(request):
    if request.method == 'POST':
        form = PartCategoryEditForm(request.POST)
        if form.is_valid():
            pc = form.cleaned_data['pc']
            if pc:
                pc.name = form.cleaned_data['pcname']
                pc.description = form.cleaned_data['pcdesc']
                title = 'Part Categories - Edit'
                notes = 'Part Category <b>' + str(pc) + '</b> edited OK'
            else:
                pc = PartCategory(
                    name = form.cleaned_data['pcname'],
                    description = form.cleaned_data['pcdesc']
                )
                title = 'Part Categories - New'
                notes = 'Part Category <b>' + str(pc) + '</b> created OK'
            pc.save()
            return done(request, title, notes, 2)
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'new' in request.GET:
            form = PartCategoryEditForm()
            title = 'Part Categories - New'
        else:
            if 'pcid' not in request.GET:
                return errmsg(request, 'Part Category ID must be specified')
            if PartCategory.objects.filter(id=request.GET.get('pcid')).count() != 1:
                return errmsg(request, 'Part Category not found in database')
            pc = PartCategory.objects.get(id=request.GET.get('pcid'))
            form = PartCategoryEditForm( \
                initial={
                    'pc': pc,
                    'pcname': pc.name,
                    'pcdesc': pc.description
                }
            )
            title = 'Part Categories - Edit'
        context = { \
            'title': title,
            'navbar1': navbar1,
            'form': form,
            'form_action': '/part_categories/edit/'
            }
        return render(request, 'base.html', context)

def part_categories_delete(request):
    if request.method == 'POST':
        form = PartCategoryConfirmForm(request.POST)
        if form.is_valid():
            try:
                pc = form.cleaned_data['pc']
                notes = 'Part Category <b>' + str(pc) + '</b> deleted OK'
                pc.delete()
                return done(request, 'Part Categories - Delete', notes, 2)
            except:
                return errmsg(request, 'Failed to delete Part Category (may be in use)')
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'pcid' not in request.GET:
            return errmsg(request, 'Part Category ID must be specified')
        if PartCategory.objects.filter(id=request.GET.get('pcid')).count() != 1:
            return errmsg(request, 'Part Category not found in database')
        pc = PartCategory.objects.get(id=request.GET.get('pcid'))
        form = PartCategoryConfirmForm( \
            initial={
                'pc': pc,
                'pcname': pc.name,
                'pcdesc': pc.description
            }
        )
        context = { \
            'title': 'Part Categories - Delete',
            'navbar1': navbar1,
            'form': form,
            'form_action': '/part_categories/delete/'
            }
        return render(request, 'base.html', context)