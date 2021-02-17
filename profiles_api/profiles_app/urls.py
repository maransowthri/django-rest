from django.urls import path
from profiles_app.views import HelloAPIView

urlpatterns = [
    path('usernames/', HelloAPIView.as_view())
]