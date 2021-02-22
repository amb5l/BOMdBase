from django import forms

class FileImportForm(forms.Form):
    def __init__(self, formats=[], *args, **kwargs):
        super(FileImportForm, self).__init__(*args, **kwargs)
    file = forms.FileField(
        label='Select a file:',
        required=False
    )