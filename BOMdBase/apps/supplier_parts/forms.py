from django import forms

from .models import SupplierPart

from organizations.models import Organization
from manufacturer_parts.models import ManufacturerPart
from part_categories.models import PartCategory

class SupplierPartBaseForm(forms.Form):
    sp = forms.ModelChoiceField(
        widget = forms.HiddenInput(),
        required=False,
        queryset=SupplierPart.objects.all()
    )
    sporg = forms.ModelChoiceField(
        label='Supplier Name',
        queryset=Organization.objects.filter(supplier=True).order_by('name')
    )
    spn = forms.CharField(
        label='Supplier Part Number'
    )
    spcat = forms.ModelChoiceField(
        label='Supplier Part Category',
        required=False,
        queryset=PartCategory.objects.order_by('name')
    )
    spdesc = forms.CharField(
        label='Supplier Part Description',
        required=False
    )
    spmp = forms.ModelChoiceField(
        label='Manufacturer Part',
        required=False,
        queryset=ManufacturerPart.objects.order_by(
            'organization__name', 'part_number')
    )
    spmpqty = forms.IntegerField(
        label='Manufacturer Part Quantity',
        required=False
    )

class SupplierPartEditForm(SupplierPartBaseForm):
    pass

class SupplierPartConfirmForm(SupplierPartBaseForm):
    def __init__(self, *args, **kwargs):
        super(SupplierPartConfirmForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if f != 'sp':
                self.fields[f].required=False
                self.fields[f].disabled=True

class SupplierPartLinkBreakForm(SupplierPartConfirmForm):
    pass

class SupplierPartLinkCreateForm(SupplierPartLinkBreakForm):
    mp = forms.ModelChoiceField(
        widget = forms.HiddenInput(),
        required=False,
        queryset=ManufacturerPart.objects.all()
    )
    def __init__(self, *args, **kwargs):
        super(SupplierPartLinkCreateForm, self).__init__(*args, **kwargs)
        self.fields['mp'].disabled=False
        self.fields['spmpqty'].required=True
        self.fields['spmpqty'].disabled=False