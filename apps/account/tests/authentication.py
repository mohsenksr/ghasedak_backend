import json

from faker import Faker
from rest_framework.reverse import reverse

from apps.account.models import User, UserRoles, Vendor
from apps.shared.test import BaseAPITestCase
from nilmal.settings.components.constants import SIGN_UP_TOKEN_PREFIX
from utils.general.cache_handler import check_in_cache, get_from_cache


class AuthenticationTest(BaseAPITestCase):
    @staticmethod
    def create_user(role):
        fake = Faker()
        password = fake.bothify(text='P@ss##??##')
        user = User.objects.create_user(first_name=fake.first_name(),
                                        last_name=fake.last_name(),
                                        phone='09123456789',
                                        email=fake.free_email(),
                                        role=role,
                                        password=password,
                                        username=fake.user_name())
        return user, password

    def test_password_signin(self):
        user, password = self.create_user('CUSTOMER')
        result = self.client.post(reverse('sign-in'), data={
            'username': user.username,
            'password': password
        })
        self.assertEqual(result.status_code, 200)
        self.assertIn('access', result.data)
    #
    # def test_verify_code_signin(self):
    #     user, password = self.create_user('CUSTOMER')
    #     result = self.client.get(reverse('send-code', kwargs={'phone': user.phone}))
    #     self.assertEqual(result.status_code, 200)
    #     self.assertTrue(check_in_cache(user.phone))
    #     result = self.client.post(
    #         reverse('verify-code'),
    #         data={
    #             'phone': user.phone,
    #             'code': get_from_cache(user.phone)
    #         })
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('access', result.data)
    #
    # def test_verify_code_signup(self):
    #     fake = Faker()
    #     phone = '09123456789'
    #     result = self.client.get(reverse('send-code', kwargs={'phone': phone}))
    #     self.assertEqual(result.status_code, 200)
    #     self.assertTrue(check_in_cache(phone))
    #     result = self.client.post(
    #         reverse('verify-code'),
    #         data={
    #             'phone': phone,
    #             'code': get_from_cache(phone)
    #         })
    #     self.assertEqual(result.status_code, 200)
    #     self.assertTrue(check_in_cache(SIGN_UP_TOKEN_PREFIX + phone, result.data['signup_token']))
    #     self.assertIn('signup_token', result.data)
    #
    # def test_verify_signup(self):
    #     fake = Faker()
    #     phone = '09123456789'
    #     result = self.client.get(reverse('send-code', kwargs={'phone': phone}))
    #     self.assertEqual(result.status_code, 200)
    #     result = self.client.post(
    #         reverse('verify-code'),
    #         data={
    #             'phone': phone,
    #             'code': get_from_cache(phone)
    #         })
    #     self.assertEqual(result.status_code, 200)
    #     result = self.client.post(
    #         reverse('sign-up'),
    #         data={
    #             "token": get_from_cache(SIGN_UP_TOKEN_PREFIX  + phone),
    #             "first_name": fake.first_name(),
    #             "last_name": fake.last_name(),
    #             "email": fake.free_email(),
    #             "password": "gholamEH@zrat22",
    #             "role": "CUSTOMER"
    #         }
    #     )
    #     self.assertEqual(result.status_code, 200)
    #     self.assertObjectKeysEqual(result.data, json.loads(mock_user_info))

    def test_refresh_token(self):
        user, password = self.create_user('CUSTOMER')
        result = self.client.post(reverse('sign-in'), data={
            'username': user.username,
            'password': password
        })
        result = self.client.post(reverse('token-refresh'), data={
            'refresh': result.data['refresh']
        })
        self.assertEqual(result.status_code, 200)
        self.assertIn('access', result.data)

    def test_sign_out(self):
        pass


mock_user_info = '{"id": 12, "username": "09888247353", "full_name": "Steven Guerrero", "first_name": "Steven", ' \
                 '"last_name": "Guerrero", "phone": "09888247353", "email": "dawnhodge@gmail.com", "avatar": null, ' \
                 '"credit": 0, "role": "CUSTOMER"} '
