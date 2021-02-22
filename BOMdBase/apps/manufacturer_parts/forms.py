from django import forms

from .models import ManufacturerPart

from organizations.models import Organization
from part_categories.models import PartCategory
from part_units.models import PartUnit

from supplier_parts.forms import SupplierPartConfirmForm

class ManufacturerPartBaseForm(forms.Form):
    mp = forms.ModelChoiceField(
        widget = forms.HiddenInput(),
        required=False,
        queryset=ManufacturerPart.objects.all()
    )
    mporg = forms.ModelChoiceField(
        label='Manufacturer',
        queryset=Organization.objects.filter(manufacturer=True) \
            .order_by('name')
    )
    mpn = forms.CharField(
        label='Manufacturer Part Number'
    )
    mpcat = forms.ModelChoiceField(
        label='Manufacturer Part Category',
        required=False,
        queryset=PartCategory.objects.order_by('name')
    )
    mpdesc = forms.CharField(
        label='Manufacturer Part Description',
        required=False
    )
    mpunit = forms.ModelChoiceField(
        label='Manufacturer Part Units',
        required=False,
        queryset=PartUnit.objects.order_by('name')
    )

class ManufacturerPartEditForm(ManufacturerPartBaseForm):
    pass

class ManufacturerPartConfirmForm(ManufacturerPartBaseForm):
    def __init__(self, *args, **kwargs):
        super(ManufacturerPartConfirmForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if f != 'mp':
                self.fields[f].required=False
                self.fields[f].disabled=True

class ManufacturerPartLinkBreakForm(SupplierPartConfirmForm):
    mp = forms.ModelChoiceField(
        widget = forms.HiddenInput(),
        required=False,
        queryset=ManufacturerPart.objects.all()
    )
    field_order = ['mp', 'sp',
        'spmp', 'spmpqty', 'sporg', 'spn', 'spcat', 'spdesc']
    def __init__(self, *args, **kwargs):
        super(ManufacturerPartLinkBreakForm, self).__init__(*args, **kwargs)
        self.fields['mp'].disabled=False

class ManufacturerPartLinkCreateForm(ManufacturerPartLinkBreakForm):
    def __init__(self, *args, **kwargs):
        super(ManufacturerPartLinkCreateForm, self).__init__(*args, **kwargs)
        self.fields['mp'].disabled=False
        self.fields['spmpqty'].required=True
        self.fields['spmpqty'].disabled=False