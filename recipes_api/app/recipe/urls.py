from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe.views import TagsView, IngredientsView, RecipesView


app_name = 'recipe'
router = DefaultRouter()
router.register('tags', TagsView)
router.register('ingredients', IngredientsView)
router.register('recipes', RecipesView)

urlpatterns = [
    path('', include(router.urls))
]
