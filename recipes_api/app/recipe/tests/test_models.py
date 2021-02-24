from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from recipe.models import Tag


def sample_user(name='Maran', email='maran@gma.com', password='passwewed'):
    return get_user_model().objects.create_user(
        name=name,
        email=email,
        password=password
    )


class TestRecipeModels(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_login(self.user)

    def test_create_tag(self):
        tag = Tag(user=self.user, name='Vegan')
        self.assertEqual(str(tag), tag.name)
