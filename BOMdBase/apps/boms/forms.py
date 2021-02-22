from django import forms

from .models import BOM

class BOMBaseForm(forms.Form):
    bom = forms.ModelChoiceField(
        widget = forms.HiddenInput(),
        required=False,
        queryset=BOM.objects.all()
    )
    bomname = forms.CharField(
        label='Name'
    )
    bomdesc = forms.CharField(
        label='Description',
        required=False
    )

class BOMEditForm(BOMBaseForm):
    pass

class BOMConfirmForm(BOMBaseForm):
    def __init__(self, *args, **kwargs):
        super(BOMConfirmForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if f != 'bom':
                self.fields[f].required=False
                self.fields[f].disabled=True

class BOMImportForm(forms.Form):
    name = forms.CharField(max_length=50)
    file = forms.FileField(label='OrCAD BOM file', required=False)
    create_parts = forms.BooleanField(
        label='Create nonexistent logical parts',
        required=False
    )
    dry_run = forms.BooleanField(
        label='Perform dry run',
        required=False
    )