from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import UserProfileViewSet, UserAuthView, UserScoreTableView


router = DefaultRouter()
router.register('users', UserProfileViewSet)
router.register('scores', UserScoreTableView)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserAuthView.as_view())
]

