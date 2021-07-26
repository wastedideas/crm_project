from django.test import TestCase
from django.contrib.auth.models import Group
from app_crm.models import Requests
from app_users.models import Users


class RequestsModelTest(TestCase):

    def setUp(self):
        Group.objects.create(name='customers')
        self.customer = Users.objects.create(
            username='test_user_1',
            first_name='test',
            last_name='user',
            password='Testpassword1',
        )
        self.new_request = Requests.objects.create(
            title='Test_title',
            text='Test_text',
            request_type='re',
            customer=self.customer,
        )

    def test_field_title(self):
        field_label = self.new_request._meta.get_field('title').verbose_name
        max_length = self.new_request._meta.get_field('title').max_length
        self.assertEqual(field_label, 'title')
        self.assertEqual(max_length, 150)

    def test_field_text(self):
        field_label = self.new_request._meta.get_field('text').verbose_name
        max_length = self.new_request._meta.get_field('text').max_length
        self.assertEqual(field_label, 'text')
        self.assertEqual(max_length, 10000)

    def test_field_creation_date(self):
        field_label = self.new_request._meta.get_field('creation_date').verbose_name
        self.assertEqual(field_label, 'creation date')

    def test_field_request_type(self):
        field_label = self.new_request._meta.get_field('request_type').verbose_name
        max_length = self.new_request._meta.get_field('request_type').max_length
        self.assertEqual(field_label, 'request type')
        self.assertEqual(max_length, 2)

    def test_field_request_status(self):
        field_label = self.new_request._meta.get_field('request_status').verbose_name
        max_length = self.new_request._meta.get_field('request_status').max_length
        self.assertEqual(field_label, 'request status')
        self.assertEqual(max_length, 2)

    def test_field_request_customer(self):
        field_label = self.new_request._meta.get_field('customer').verbose_name
        self.assertEqual(field_label, 'customer')

    def test_field_request_worker(self):
        field_label = self.new_request._meta.get_field('worker').verbose_name
        self.assertEqual(field_label, 'worker')

    def test_request_verbose_names(self):
        verb_name = self.new_request._meta.verbose_name
        verb_name_plural = self.new_request._meta.verbose_name_plural
        self.assertEqual(verb_name, 'request')
        self.assertEqual(verb_name_plural, 'requests')
