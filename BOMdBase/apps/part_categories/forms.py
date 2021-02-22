from django import forms

from .models import PartCategory

class PartCategoryBaseForm(forms.Form):
    pc = forms.ModelChoiceField(
        widget = forms.HiddenInput(),
        required=False,
        queryset=PartCategory.objects.all()
    )
    pcname = forms.CharField(
        label='Name'
    )
    pcdesc = forms.CharField(
        label='Description',
        required=False
    )

class PartCategoryEditForm(PartCategoryBaseForm):
    pass

class PartCategoryConfirmForm(PartCategoryBaseForm):
    def __init__(self, *args, **kwargs):
        super(PartCategoryConfirmForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if f != 'pc':
                self.fields[f].required=False
                self.fields[f].disabled=True