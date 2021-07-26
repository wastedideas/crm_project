from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth.models import Group
from app_users.models import Users
from app_users.forms import UserRegistration
from app_crm.models import Requests


class UserLoginViewTest(TestCase):

    def test_users_login_check_name_and_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/login.html')


class UserLogoutViewTest(TestCase):

    def test_users_logout_check_name_and_template(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/logout.html')


class UsersRegisterViewTest(TestCase):

    def setUp(self):
        Group.objects.create(name='customers')

    def test_user_register_check_name_and_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/register.html')

    def test_user_register_uses_correct_forms(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(
            type(
                response.context['form'],
            ),
            UserRegistration,
        )

    def test_user_register_check_redirect(self):
        data_for_test = {
            'username': 'test_user',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password1': 'Testpassword1',
            'password2': 'Testpassword1',
        }
        self.client.login(
            username='test_user',
            password='Testpassword1'
        )
        response = self.client.post(
            reverse('register'),
            data_for_test
        )
        self.assertRedirects(response, reverse('main_page'))


class UsersPersonalAreaTest(TestCase):

    def setUp(self):
        Group.objects.create(name='customers')
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
        self.client.login(
            username='test_user',
            password='Testpassword1',
        )

    def test_user_personal_area_check_name_and_template(self):
        response = self.client.get(reverse('personal_area', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/personal_area.html')

    def test_user_personal_area_check_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('personal_area', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)

    def test_create_request_check_access(self):
        response = self.client.get(reverse('personal_area', args=[self.user_1.pk]))
        self.assertEqual(response.status_code, 403)
