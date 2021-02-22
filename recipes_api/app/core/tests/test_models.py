from django.test import TestCase
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    def test_create_user_with_email(self):
        email = 'maran@gmail.com'
        password = 'pass123'
        name = "Maran K"
        user = get_user_model().objects.create_user(
            name=name,
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(password))

    def test_normalized_email(self):
        email = 'maran@GMAIL.com'
        password = 'pass123'
        name = "Maran K"
        user = get_user_model().objects.create_user(
            name=name,
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())

    def test_email_required(self):
        with self.assertRaises(ValueError):
            password = 'pass123'
            name = "Maran K"
            user = get_user_model().objects.create_user(
                email="",
                name=name,
                password=password
            )
            self.assertNotEqual(user.name, name)

    def test_super_user(self):
        email = 'maran@gmail.com'
        password = 'pass123'
        name = "Maran K"
        user = get_user_model().objects.create_superuser(
            name=name,
            email=email,
            password=password
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
