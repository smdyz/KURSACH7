from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, \
    RetrieveUpdateAPIView

from users.pagination import UserPagination
from users.permissions import IsModeratorOrOwner, IsModeratorOrSuperuser, IsOwner
from users.serializers import UserSerializer
from users.models import User
from rest_framework import permissions, status
from rest_framework.response import Response


class UserCreateAPIView(CreateAPIView):
    """
    Эндпоинт для создания пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()


class UserDestroyAPIView(DestroyAPIView):
    """
    Эндпоинт для удаления пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrOwner, IsModeratorOrSuperuser]


class UserListAPIView(ListAPIView):
    """
    Эндпоинт для просмотра списка пользователей
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrSuperuser]


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Эндпоинт для просмотра одного пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrOwner, IsModeratorOrSuperuser]


class UserProfileUpdateAPIView(RetrieveUpdateAPIView):
    """
    Эндпоинт для обновления профиля пользователя.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        if self.get_object() != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
