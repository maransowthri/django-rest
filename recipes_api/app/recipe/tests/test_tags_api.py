from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from recipe.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class TestPublicTagsAPI(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required_to_fetch_tags(self):
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateTagsAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='Maran K',
            email='maran@gmail.com',
            password='testpass@123'
        )
        self.client.force_authenticate(self.user)

    def test_fetch_tags_api(self):
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_for_loggedin_user_only(self):
        Tag.objects.create(user=self.user, name='Vegan')
        user2 = get_user_model().objects.create_user(
            name='Kavinath',
            email='kavinath@gmail.com',
            password='kaviissmiling'
        )
        Tag.objects.create(user=user2, name='Dessert')
        res = self.client.get(TAGS_URL)
        self.assertEqual(len(res.data), 1)

    def test_create_tag_successful(self):
        payload = {'name': 'Vegan'}
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tags_filter(self):
        tag1 = Tag.objects.create(user=self.user, name='Tag 1')
        tag2 = Tag.objects.create(user=self.user, name='Tag 2')
        res = self.client.get(TAGS_URL, {'assigned_only': str(tag1.id)})
        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
