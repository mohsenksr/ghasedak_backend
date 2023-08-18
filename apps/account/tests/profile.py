import json

from apps.shared.test import BaseAPITestCase
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from faker import Faker

User = get_user_model()


class ProfileTest(BaseAPITestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client.force_authenticate(user=user)

    def test_update_profile(self):
        fake = Faker()
        name = fake.word()
        response = self.client.post(reverse('profile'), data={'first_name': name})
        self.assertEqual(response.status_code, 200)
        self.assertObjectKeysEqual(response.data, json.loads(set_profile_mock_response))
        self.assertEqual(response.data['first_name'], name)

    def test_get_profile(self):
        fake = Faker()
        name = fake.word()
        res = self.client.post(reverse('profile'), data={'email': 'aaa@bbb.ccc'})
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertObjectKeysEqual(response.data, json.loads(get_profile_mock_response))


get_profile_mock_response = '{"first_name": "mamad", "last_name": "", "phone": "", "home_phone": null,' \
                            ' "email": null, "cc_number": null, "avatar": null, "role": null, "verified_vendor": true} '

set_profile_mock_response = '{"first_name": "mamad", "last_name": "", "phone": "", "home_phone": null,' \
                            ' "email": null, "cc_number": null} '
