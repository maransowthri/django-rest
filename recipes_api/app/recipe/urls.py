from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe.views import TagsView


app_name = 'recipe'
router = DefaultRouter()
router.register('tags', TagsView)

urlpatterns = [
    path('', include(router.urls))
]
