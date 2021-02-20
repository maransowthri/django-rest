from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from accounts.models import UserProfile, UserScoreTable
from accounts.serializers import UserProfileSerializer, UserScoreTableSerializer
from accounts.permissions import UserProfilePermission, UserScoreTablePermission


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UserProfilePermission,)


class UserAuthView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserScoreTableView(ModelViewSet):
    queryset = UserScoreTable.objects.all()
    serializer_class = UserScoreTableSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UserScoreTablePermission, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)