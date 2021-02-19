from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_app.views import UsersAPIView, UsersViewset


router = DefaultRouter()
router.register('usernames-viewset', UsersViewset, base_name='usernames-viewset')

urlpatterns = [
    path('usernames-api/', UsersAPIView.as_view()),
    path('', include(router.urls)),
]