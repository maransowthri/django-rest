from django.urls import path

from user.views import CreateUserView, UserTokenView, ManageUserView


app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', UserTokenView.as_view(), name='token'),
    path('myself/', ManageUserView.as_view(), name='myself')
]
