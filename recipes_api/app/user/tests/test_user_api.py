from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase


CREATE_USER_URL = reverse('user:create')


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
