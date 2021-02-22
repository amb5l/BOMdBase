from django import forms

from organizations.models import Organization

class OrganizationBaseForm(forms.Form):
    org = forms.ModelChoiceField(
        widget = forms.HiddenInput(),
        required=False,
        queryset=Organization.objects.all()
    )
    orgname = forms.CharField(
        label='Name'
    )
    org_m = forms.BooleanField(
        label='Is Manufacturer',
        required=False
    )
    org_s = forms.BooleanField(
        label='Is Supplier',
        required=False
    )
    orgurl = forms.URLField(
        label='URL',
        required=False
    )
    orgnotes = forms.CharField(
        label='Notes',
        required=False
    )

class OrganizationEditForm(OrganizationBaseForm):
    pass

class OrganizationConfirmForm(OrganizationBaseForm):
    def __init__(self, *args, **kwargs):
        super(OrganizationConfirmForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if f != 'org':
                self.fields[f].required=False
                self.fields[f].disabled=True