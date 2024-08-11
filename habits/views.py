from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from habits.models import Habits
from habits.pagination import HabitPagination
from habits.serializer import HabitsSerializer
from users.permissions import IsOwner


class HabitCreateAPIView(CreateAPIView):
    """
    Эндпоинт для создания привычки
    """
    serializer_class = HabitsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save()


class HabitListAPIView(ListAPIView):
    """
    Эндпоинт для вывода списка привычек
    """
    serializer_class = HabitsSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwner]

    def get_queryset(self):
        user = self.request.user
        if not user.is_superuser:
            queryset = Habits.objects.filter(owner=user)
        else:
            queryset = Habits.objects.all()
        return queryset


class PublicHabitListAPIView(ListAPIView):
    """
    Эндпоинт для вывода списка публичных привычек
    """
    serializer_class = HabitsSerializer
    queryset = Habits.objects.filter(is_public=True)
    pagination_class = HabitPagination


class HabitRetrieveAPIView(RetrieveAPIView):
    """
    Эндпоинт для просмотра одной привычки
    """
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwner]


class HabitUpdateAPIView(UpdateAPIView):
    """
    Эндпоинт для обновления или изменения привычки
    """
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwner]


class HabitDestroyAPIView(DestroyAPIView):
    """
    Эндпоинт для удаления привычки
    """
    queryset = Habits.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwner]
