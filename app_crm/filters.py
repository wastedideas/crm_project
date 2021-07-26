import django_filters
from django import forms
from app_crm.models import Requests


class RequestsFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['creation_date__contains'] = forms.DateField(
            label='Creation date exact',
            required=False,
        )
        self.form.fields['creation_date__contains'].input_formats = ['%d.%m.%Y']
        self.form.fields['creation_date__contains'].widget.attrs = {'placeholder': 'DD.MM.YYYY'}

        date_from_field = self.form.fields['creation_date'].fields[0]
        date_to_field = self.form.fields['creation_date'].fields[1]
        date_from_field.input_formats = ['%d.%m.%Y']
        date_to_field.input_formats = ['%d.%m.%Y']

    creation_date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={
                'placeholder': 'DD.MM.YYYY',
            },
        ),
    )
    request_status = django_filters.MultipleChoiceFilter(
        choices=Requests.REQUEST_STATUS,
        widget=forms.CheckboxSelectMultiple,
    )
    request_type = django_filters.ChoiceFilter(
        choices=Requests.REQUEST_TYPE,
        empty_label='all',
    )

    class Meta:
        model = Requests
        fields = {
            'creation_date': ['contains', 'exact'],
            'request_status': ['exact'],
            'request_type': ['exact'],
        }
