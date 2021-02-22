from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Organization
from .tables import organizations_table
from .forms import OrganizationEditForm, OrganizationConfirmForm

from main.shared import navbar1
from main.flextable import flextable
from main.utils import errmsg, done

def organizations(request):
    table = flextable(
        request.GET,
        organizations_table,
        Organization.objects.all()
    )
    context = { \
        'title': 'Organizations',
        'navbar1': navbar1,
        'navbar2': [('create new organization', 'edit?new')],
        'table': table,
        }
    return render(request, 'base.html', context)

def organizations_edit(request):
    if request.method == 'POST':
        form = OrganizationEditForm(request.POST)
        if form.is_valid():
            org = form.cleaned_data['org']
            if org:
                org.name = form.cleaned_data['orgname']
                org.manufacturer = form.cleaned_data['org_m']
                org.supplier = form.cleaned_data['org_s']
                org.notes = form.cleaned_data['orgnotes']
                title = 'Organizations - Edit'
                notes = 'Organization <b>' + str(org) + '</b> edited OK'
            else:
                org = Organization(
                    name = form.cleaned_data['orgname'],
                    manufacturer = form.cleaned_data['org_m'],
                    supplier = form.cleaned_data['org_s'],
                    notes = form.cleaned_data['orgnotes']
                )
                title = 'Organizations - New'
                notes = 'Organization <b>' + str(org) + '</b> created OK'
            org.save()
            return done(request, title, notes, 2)
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'new' in request.GET:
            form = OrganizationEditForm()
            title = 'Organizations - New'
        else:
            if 'orgid' not in request.GET:
                return errmsg(request, 'Organization ID must be specified')
            if Organization.objects.filter(id=request.GET.get('orgid')).count() != 1:
                return errmsg(request, 'Organization not found in database')
            org = Organization.objects.get(id=request.GET.get('orgid'))
            form = OrganizationEditForm( \
                initial={
                    'org': org,
                    'orgname': org.name,
                    'org_m': org.manufacturer,
                    'org_s': org.supplier,
                    'orgurl': org.url,
                    'orgnotes': org.notes
                }
            )
            title = 'Organizations - Edit'
        context = { \
            'title': title,
            'navbar1': navbar1,
            'form': form,
            'form_action': '/organizations/edit/'
            }
        return render(request, 'base.html', context)

def organizations_delete(request):
    if request.method == 'POST':
        form = OrganizationConfirmForm(request.POST)
        if form.is_valid():
            try:
                org = form.cleaned_data['org']
                notes = 'Organization <b>' + str(org) + '</b> deleted OK'
                org.delete()
                return done(request, 'Organizations - Delete', notes, 2)
            except:
                return errmsg(request, 'Failed to delete Organization (may be in use)')
        else:
            print(form.errors) # todo: improve
            return errmsg(request, 'Form contains errors')
    else:
        if 'orgid' not in request.GET:
            return errmsg(request, 'Organization ID must be specified')
        if Organization.objects.filter(id=request.GET.get('orgid')).count() != 1:
            return errmsg(request, 'Organization not found in database')
        org = Organization.objects.get(id=request.GET.get('orgid'))
        form = OrganizationConfirmForm( \
            initial={
                'org': org,
                'orgname': org.name,
                'org_m': org.manufacturer,
                'org_s': org.supplier,
                'orgurl': org.url,
                'orgnotes': org.notes
            }
        )
        context = { \
            'title': 'Organizations - Delete',
            'navbar1': navbar1,
            'form': form,
            'form_action': '/organizations/delete/'
            }
        return render(request, 'base.html', context)