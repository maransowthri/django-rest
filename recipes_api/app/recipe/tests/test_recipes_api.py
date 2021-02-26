from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from recipe.models import Recipe, Ingredient, Tag
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')
RECIPE_DEFAULTS = {
    'title': 'Masal Dosa',
    'time_minutes': 10,
    'price': 7.86
}


def get_recipe_detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name='Main Course'):
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Cinnamon'):
    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    defaults = {
        'title': 'Sample Title',
        'price': 5.65,
        'time_minutes': 6
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


class TestPublicRecipesAPI(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required_to_fetch_recipes(self):
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateRecipesAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='Kalees R',
            email='kalees@gmail.com',
            password='sdf3^wg'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_recipes_success(self):
        Recipe.objects.create(
            user=self.user,
            **RECIPE_DEFAULTS
        )
        Recipe.objects.create(
            user=self.user,
            **RECIPE_DEFAULTS
        )
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe_to_corresponding_user(self):
        Recipe.objects.create(
            user=self.user,
            **RECIPE_DEFAULTS
        )
        user2 = get_user_model().objects.create_user(
            name='Karan K',
            email='karan@fmsd.cid',
            password='sdkjshd'
        )
        Recipe.objects.create(
            user=user2,
            **RECIPE_DEFAULTS
        )
        res = self.client.get(RECIPES_URL)
        self.assertEqual(len(res.data), 1)

    def test_view_recipe_detail(self):
        recipe = sample_recipe(user=self.user)
        recipe.ingredients.add(sample_ingredient(user=self.user))
        recipe.tags.add(sample_tag(user=self.user))

        res = self.client.get(get_recipe_detail_url(recipe.id))
        serializer = RecipeDetailSerializer(recipe)
        self.assertEquals(res.data, serializer.data)

    def test_post_recipes(self):
        tag = sample_tag(user=self.user)
        ingredient = sample_ingredient(user=self.user)
        RECIPE_DEFAULTS['tags'] = [tag.id]
        RECIPE_DEFAULTS['ingredients'] = [ingredient.id]
        res = self.client.post(RECIPES_URL, RECIPE_DEFAULTS)
        recipe = Recipe.objects.get(
            user=self.user,
            title=RECIPE_DEFAULTS['title']
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(recipe is not None)
        self.assertEqual(
            recipe.tags.all().count(),
            len(RECIPE_DEFAULTS['tags'])
        )
        self.assertEqual(
            recipe.ingredients.all().count(),
            len(RECIPE_DEFAULTS['ingredients'])
        )

    def test_partial_update_recipe(self):
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name='Curry')
        payload = {
            'title': 'Chicken Tikka',
            'tags': [new_tag.id]
        }
        url = get_recipe_detail_url(recipe.id)
        self.client.patch(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        tags = recipe.tags.all()
        self.assertIn(new_tag, tags)

    def test_full_update_recipe(self):
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        payload = {
            'title': 'Chicken Tikka',
            'price': 6.77,
            'time_minutes': 12
        }
        self.client.put(get_recipe_detail_url(recipe.id), payload)
        recipe.refresh_from_db()
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
