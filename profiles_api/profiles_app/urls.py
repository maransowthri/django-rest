from django.urls import path
from profiles_app.views import UsersAPIView

urlpatterns = [
    path('usernames/', UsersAPIView.as_view())
]