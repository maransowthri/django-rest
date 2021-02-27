from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch

from recipe.models import Tag, Ingredient, Recipe
from recipe import models


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

    @patch('uuid.uuid4')
    def test_recipe_image_filename(self, mock_uuid):
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.get_recipe_filepath(None, 'my-image.jpg')
        exp_path = f'/uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
