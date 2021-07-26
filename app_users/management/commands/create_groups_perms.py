from itertools import chain
from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from app_users.models import Users


class Command(BaseCommand):
    help = 'Creating groups and permissions'

    def handle(self, *args, **options):
        new_worker = Users.objects.create(
            username='first_worker',
            first_name='first_worker_name',
            last_name='first_worker_last_name',
            password='Firstworker1',
        )
        workers_group, is_create = Group.objects.get_or_create(name='workers')
        customers_group, is_create = Group.objects.get_or_create(name='customers')
        workers_perms = list(
            chain(
                Permission.objects.filter(content_type__app_label='app_crm'),
                Permission.objects.filter(content_type__app_label='app_users'),
            )
        )
        customers_perms = Permission.objects.get(codename='add_requests')
        customers_group.permissions.add(customers_perms)
        for i_perm in workers_perms:
            workers_group.permissions.add(i_perm)
        new_worker.groups.add(workers_group)
