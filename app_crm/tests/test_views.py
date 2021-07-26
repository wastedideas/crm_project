from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from app_crm.models import Requests
from app_users.models import Users
from app_crm.forms import EditRequestForm


class RequestCreateViewTest(TestCase):

    def setUp(self):
        self.workers_group = Group.objects.create(name='workers')
        self.customers_group = Group.objects.create(name='customers')
        self.customers_perms = Permission.objects.get(codename='add_requests')
        self.customers_group.permissions.add(self.customers_perms)
        self.user = Users.objects.create_user(
            username='test_user',
            first_name='test',
            last_name='user',
            password='Testpassword1',
        )
        self.worker = Users.objects.create_user(
            username='test_user_1',
            first_name='test',
            last_name='user',
            password='Testpassword1',
        )
        self.worker.groups.add(self.workers_group)
        self.client.login(
            username='test_user',
            password='Testpassword1',
        )

    def test_create_request_check_name_and_template(self):
        response = self.client.get(reverse('create_request'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_crm/create_or_edit_request.html')

    def test_create_request_check_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('create_request'))
        self.assertEqual(response.status_code, 302)

    def test_create_request_check_permissions(self):
        self.customers_group.permissions.clear()
        response = self.client.get(reverse('create_request'))
        self.assertEqual(response.status_code, 403)

    def test_create_request_check_redirect(self):
        data_for_test = {
            'title': 'test_title',
            'text': 'test_description',
            'request_type': 're',
            'customer': self.user,
            'worker': self.user,
        }
        response = self.client.post(reverse('create_request'), data_for_test)
        self.assertRedirects(response, reverse('main_page'))


class RequestDetailEditDeleteViewTest(TestCase):

    def setUp(self):
        Group.objects.create(name='customers')
        self.workers_group = Group.objects.create(name='workers')
        self.workers_perms = Permission.objects.get(codename='change_requests')
        self.workers_group.permissions.add(self.workers_perms)
        self.workers_group.permissions.add(Permission.objects.get(codename='delete_requests'))
        self.user = Users.objects.create_user(
            username='test_user',
            first_name='test',
            last_name='user',
            password='Testpassword1',
        )
        self.user_1 = Users.objects.create_user(
            username='test_user_1',
            first_name='test',
            last_name='user',
            password='Testpassword1',
        )
        self.user.groups.add(self.workers_group)

        self.client.login(
            username='test_user',
            password='Testpassword1',
        )
        self.new_request = Requests.objects.create(
            title='test_request',
            text='text_text',
            request_type='re',
            request_status='op',
            customer=self.user,
            worker=self.user,
        )

    def test_detail_request_check_name_and_template(self):
        response = self.client.get(reverse('request_detail', args=[self.new_request.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_crm/request_detail.html')

    def test_detail_request_check_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('request_detail', args=[self.new_request.pk]))
        self.assertEqual(response.status_code, 302)

    def test_detail_request_check_permissions(self):
        self.client.login(
            username='test_user_1',
            password='Testpassword1',
        )
        response = self.client.get(reverse('request_detail', args=[self.new_request.pk]))
        self.assertEqual(response.status_code, 403)

    def test_edit_request_check_name_and_template(self):
        response = self.client.get(reverse('edit_request', args=[self.new_request.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_crm/create_or_edit_request.html')

    def test_edit_request_check_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('edit_request', args=[self.new_request.pk]))
        self.assertEqual(response.status_code, 302)

    def test_edit_request_check_permissions(self):
        self.workers_group.permissions.clear()
        response = self.client.get(reverse('edit_request', args=[self.new_request.pk]))
        self.assertEqual(response.status_code, 403)

    def test_edit_request_uses_correct_forms(self):
        response = self.client.get(reverse('edit_request', args=[self.new_request.pk]))
        self.assertEqual(
            type(
                response.context['form'],
            ),
            EditRequestForm,
        )

    def test_delete_request_check_name_and_template(self):
        response = self.client.get(reverse('delete_request', args=[self.new_request.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_crm/delete_request.html')

    def test_delete_request_check_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('delete_request', args=[self.new_request.pk]))
        self.assertEqual(response.status_code, 302)

    def test_delete_request_check_permissions(self):
        self.workers_group.permissions.clear()
        response = self.client.get(reverse('delete_request', args=[self.new_request.pk]))
        self.assertEqual(response.status_code, 403)


class RequestsListViewTest(TestCase):

    def setUp(self):
        self.workers_group = Group.objects.create(name='workers')
        Group.objects.create(name='customers')
        self.workers_perms = Permission.objects.get(codename='view_requests_list')
        self.workers_group.permissions.add(self.workers_perms)
        self.user = Users.objects.create_user(
            username='test_user',
            first_name='test',
            last_name='user',
            password='Testpassword1',
        )
        self.user.groups.add(self.workers_group)
        self.client.login(
            username='test_user',
            password='Testpassword1',
        )

    def test_requests_list_check_name_and_template(self):
        response = self.client.get(reverse('requests_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_crm/requests_list.html')

    def test_requests_list_check_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('create_request'))
        self.assertEqual(response.status_code, 302)

    def test_requests_list_check_permissions(self):
        self.workers_group.permissions.clear()
        response = self.client.get(reverse('create_request'))
        self.assertEqual(response.status_code, 403)
