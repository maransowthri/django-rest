from rest_framework import generics
from django.contrib.auth import get_user_model

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
