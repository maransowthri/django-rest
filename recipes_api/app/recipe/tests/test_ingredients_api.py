from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class TestPublicIngredientsAPI(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required_to_fetch_ingredients(self):
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateIngredientsAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='Maran K',
            email='marank@gmail.com',
            password='pass2ew23'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_ingredients_success(self):
        Ingredient.objects.create(user=self.user, name='Beans')
        Ingredient.objects.create(user=self.user, name='Carrot')
        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_to_loggedin_user(self):
        Ingredient.objects.create(user=self.user, name='Carrot')
        user2 = get_user_model().objects.create_user(
            name='Karan K',
            email='karan@gmail.com',
            password='Kakjfd@232'
        )
        Ingredient.objects.create(user=user2, name='Beans')
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(len(res.data), 1)

    def test_post_ingredients_success(self):
        payload = {'name': 'Carrot'}
        self.client.post(INGREDIENTS_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        )
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
