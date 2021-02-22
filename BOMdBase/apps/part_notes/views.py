from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import PartNote
from .tables import part_notes_table
from .forms import PartNoteEditForm, PartNoteConfirmForm

from main.shared import navbar1
from main.flextable import flextable
from main.utils import errmsg, done

def part_notes(request):
    table = flextable(
        request.GET,
        part_notes_table,
        PartNote.objects.all()
    )
    context = { \
        'title': 'Part Notes',
        'navbar1': navbar1,
        'navbar2': [
            ('categories', '/part_categories'),
            ('units', '/part_notes'),
            ('create new note', 'edit?new')
        ],
        'table': table,
        }
    return render(request, 'base.html', context)

def part_notes_edit(request):
    if request.method == 'POST':
        form = PartNoteEditForm(request.POST)
        if form.is_valid():
            pn = form.cleaned_data['pn']
            if pn:
                pn.note = form.cleaned_data['pnnote']
                title = 'Part Notes - Edit'
                notes = 'Part Note edited OK'
            else:
                pn = PartNote(note = form.cleaned_data['pnnote'])
                title = 'Part Notes - New'
                notes = 'Part Note created OK'
            pn.save()
            return done(request, title, notes, 2)
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'new' in request.GET:
            form = PartNoteEditForm()
            title = 'Part Notes - New'
        else:
            if 'pnid' not in request.GET:
                return errmsg(request, 'Part Note ID must be specified')
            if PartNote.objects.filter(id=request.GET.get('pnid')).count() != 1:
                return errmsg(request, 'Part Note not found in database')
            pn = PartNote.objects.get(id=request.GET.get('pnid'))
            form = PartNoteEditForm(initial={'pn': pn, 'pnnote': pn.note})
            title = 'Part Notes - Edit'
        context = { \
            'title': title,
            'navbar1': navbar1,
            'form': form,
            'form_action': '/part_notes/edit/'
            }
        return render(request, 'base.html', context)

def part_notes_delete(request):
    if request.method == 'POST':
        form = PartNoteConfirmForm(request.POST)
        if form.is_valid():
            try:
                pn = form.cleaned_data['pn']
                notes = 'Part Note deleted OK'
                pn.delete()
                return done(request, 'Part Notes - Delete', notes, 2)
            except:
                return errmsg(request, 'Failed to delete Part Note (may be in use)')
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'pnid' not in request.GET:
            return errmsg(request, 'Part Note ID must be specified')
        if PartNote.objects.filter(id=request.GET.get('pnid')).count() != 1:
            return errmsg(request, 'Part Note not found in database')
        pn = PartNote.objects.get(id=request.GET.get('pnid'))
        form = PartNoteEditForm(initial={'pn': pn, 'pnnote': pn.note})
        context = { \
            'title': 'Part Notes - Delete',
            'navbar1': navbar1,
            'form': form,
            'form_action': '/part_notes/delete/'
            }
        return render(request, 'base.html', context)