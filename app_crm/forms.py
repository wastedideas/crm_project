from django import forms
from app_crm.models import Requests
from app_users.models import Users


class EditRequestForm(forms.ModelForm):
    worker = forms.ModelChoiceField(
        queryset=Users.objects.filter(groups__name='workers'),
        empty_label='not selected',
    )

    class Meta:
        model = Requests
        exclude = ('customer', )
