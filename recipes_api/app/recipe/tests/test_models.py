from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from recipe.models import Tag, Ingredient, Recipe


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
        tag = Tag.objects.create(user=self.user, name='Vegan')
        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        ingredient = Ingredient.objects.create(user=self.user, name='Cucumber')
        self.assertEqual(str(ingredient), ingredient.name)

    def test_create_recipe(self):
        recipe = Recipe.objects.create(
            user=self.user,
            title='Mushroom Dosa',
            time_minutes=5,
            price=8.00
        )
        self.assertEqual(str(recipe), recipe.title)
