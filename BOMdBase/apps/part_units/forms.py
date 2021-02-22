from django import forms

from .models import PartUnit

class PartUnitBaseForm(forms.Form):
    pu = forms.ModelChoiceField(
        widget = forms.HiddenInput(),
        required=False,
        queryset=PartUnit.objects.all()
    )
    puname = forms.CharField(
        label='Name'
    )
    pudesc = forms.CharField(
        label='Description',
        required=False
    )

class PartUnitEditForm(PartUnitBaseForm):
    pass

class PartUnitConfirmForm(PartUnitBaseForm):
    def __init__(self, *args, **kwargs):
        super(PartUnitConfirmForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if f != 'pu':
                self.fields[f].required=False
                self.fields[f].disabled=True