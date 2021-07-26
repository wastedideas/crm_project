from django.contrib import admin
from app_users.models import Users


class UsersAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'first_name',
        'last_name',
    ]


admin.site.register(Users, UsersAdmin)
