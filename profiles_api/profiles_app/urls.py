from django.urls import path, include
from rest_framework.routers import DefaultRouter

from profiles_app.views import TestAPIView, TestViewSet, UserProfileViewSet, UserAuthView, UserProfileFeedViewSet


router = DefaultRouter()
router.register('usernames-viewset', TestViewSet, base_name='usernames-viewset')
router.register('profiles-viewset', UserProfileViewSet, base_name='profile-viewset')
router.register('feeds-viewset', UserProfileFeedViewSet, base_name='feeds-viewset')

urlpatterns = [
    path('usernames-api/', TestAPIView.as_view()),
    path('', include(router.urls)),
    path('login/', UserAuthView.as_view())
]