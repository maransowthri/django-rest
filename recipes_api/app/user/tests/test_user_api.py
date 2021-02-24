from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
MY_USER_URL = reverse('user:myself')


class PublicUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'name': 'Maran K',
            'password': 'pass1wqiueyiqw23',
            'email': 'maradsfn@gmail.com'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))

    def test_create_user_exists(self):
        payload = {
            'name': 'Maran K',
            'password': 'pass1wqiueyiqw23',
            'email': 'maran@gmail.com'
        }
        get_user_model().objects.create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_short(self):
        payload = {
            'name': 'Maran K',
            'password': 'pw',
            'email': 'maran453@gmail.com'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
                        email=payload['email']
                      ).exists()
        self.assertFalse(user_exists)

    def test_create_user_token_success(self):
        payload = {
            'name': 'Maran K',
            'email': 'maran@gmail.com',
            'password': 'testpass1234'
        }
        get_user_model().objects.create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_token_invalid_password(self):
        payload = {
            'name': 'Maran K',
            'email': 'maran@gmail.com',
            'password': 'pass1234'
        }
        get_user_model().objects.create_user(**payload)
        payload['password'] = 'wrongpass'
        res = self.client.post(TOKEN_URL, **payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_token_user_nonexist(self):
        payload = {
            'name': 'Maran K',
            'email': 'maran@gmail.com',
            'password': 'pass1234'
        }
        res = self.client.post(TOKEN_URL, **payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_authentication_needed(self):
        res = self.client.get(MY_USER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'name': 'Maran K',
            'email': 'maran@gmail.com',
            'password': 'testpass123'
        }
        self.user = get_user_model().objects.create_user(**self.payload)
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        res = self.client.get(MY_USER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_not_allowed_on_get_user_profile(self):
        res = self.client.post(MY_USER_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_details(self):
        payload = {
            'name': 'New Name',
            'password': 'NewPass@123'
        }
        res = self.client.patch(MY_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
