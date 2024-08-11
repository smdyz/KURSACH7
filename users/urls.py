from django.urls import path
from users.views import UserCreateAPIView, UserDestroyAPIView, UserListAPIView, UserRetrieveAPIView, \
    UserProfileUpdateAPIView
from users.apps import UsersConfig
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )

app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
    path('<int:pk>/update/', UserProfileUpdateAPIView.as_view(), name='user_update'),
    path('<int:pk>/destroy/', UserDestroyAPIView.as_view(), name='user_destroy'),
    path('user/', UserListAPIView.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
]
