from django import forms

from .models import PartNote

class PartNoteBaseForm(forms.Form):
    pn = forms.ModelChoiceField(
        widget = forms.HiddenInput(),
        required=False,
        queryset=PartNote.objects.all()
    )
    pnnote = forms.CharField(
        label='Note'
    )

class PartNoteEditForm(PartNoteBaseForm):
    pass

class PartNoteConfirmForm(PartNoteBaseForm):
    def __init__(self, *args, **kwargs):
        super(PartNoteConfirmForm, self).__init__(*args, **kwargs)
        self.fields['pnnote'].required=False
        self.fields['pnnote'].disabled=True