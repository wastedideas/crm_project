from django.test import TestCase
from app_users.models import Users
from django.contrib.auth.models import Group


class UserModelTest(TestCase):

    def setUp(self):
        Group.objects.create(name='customers')
        self.customer = Users.objects.create(
            username='test_user',
            first_name='test',
            last_name='user',
        )

    def test_users_model_unique_code(self):
        field_label = self.customer._meta.get_field('unique_code').verbose_name
        max_length = self.customer._meta.get_field('unique_code').max_length
        self.assertEqual(field_label, 'unique code')
        self.assertEqual(max_length, 36)

    def test_users_model_chat_id(self):
        field_label = self.customer._meta.get_field('chat_id').verbose_name
        self.assertEqual(field_label, 'chat id')

    def test_users_verbose_names(self):
        verb_name = self.customer._meta.verbose_name
        verb_name_plural = self.customer._meta.verbose_name_plural
        self.assertEqual(verb_name, 'user')
        self.assertEqual(verb_name_plural, 'users')

    def test_object_name(self):
        object_name = f'{self.customer.first_name} {self.customer.last_name}'
        self.assertEquals(object_name, str(self.customer))
