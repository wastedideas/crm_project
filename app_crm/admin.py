from django.contrib import admin
from app_crm.models import Requests


class RequestsAdmin(admin.ModelAdmin):
    list_filter = [
        'creation_date',
        'request_type',
        'request_status',
    ]


admin.site.register(Requests, RequestsAdmin)
