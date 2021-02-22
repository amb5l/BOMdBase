from django import forms

from .models import LogicalPart

from part_categories.models import PartCategory
from part_notes.models import PartNote

class LogicalPartBaseForm(forms.Form):
    lp = forms.ModelChoiceField(
        widget = forms.HiddenInput(),
        required=False,
        queryset=LogicalPart.objects.all()
    )
    lpn = forms.CharField(
        label='Logical Part Number'
    )
    lpcat = forms.ModelChoiceField(
        label='Logical Part Category',
        required=False,
        queryset=PartCategory.objects.order_by('name')
    )
    lpdesc = forms.CharField(
        label='Logical Part Description',
        required=False
    )
    lpnotes = forms.ModelChoiceField(
        label='Logical Part Notes',
        required=False,
        queryset=PartNote.objects.order_by('note')
    )

class LogicalPartEditForm(LogicalPartBaseForm):
    pass

class LogicalPartConfirmForm(LogicalPartBaseForm):
    def __init__(self, *args, **kwargs):
        super(LogicalPartConfirmForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if f != 'lp':
                self.fields[f].required=False
                self.fields[f].disabled=True