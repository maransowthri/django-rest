from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe.views import TagsView, ingredientsView


app_name = 'recipe'
router = DefaultRouter()
router.register('tags', TagsView)
router.register('ingredients', ingredientsView)

urlpatterns = [
    path('', include(router.urls))
]
