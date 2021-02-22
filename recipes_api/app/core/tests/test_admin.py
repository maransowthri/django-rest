from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestAdmin(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            name="Maran K",
            email="admin@gmail.com",
            password="pass123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            name="Sowthri K",
            email="sowthri@gmail.com",
            password="pass123"
        )

    def test_users_listed(self):
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_page_change(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
