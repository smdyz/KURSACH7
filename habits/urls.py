from habits.apps import HabitsConfig
from django.urls import path
from habits.views import HabitCreateAPIView, HabitListAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, \
    HabitDestroyAPIView, PublicHabitListAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('',PublicHabitListAPIView.as_view(),name='pablichabit_list'),
    path('create/',HabitCreateAPIView.as_view(),name='habit_create'),
    path('list/',HabitListAPIView.as_view(),name='habits_list'),
    path('view/<int:pk>',HabitRetrieveAPIView.as_view(),name='habit_detail'),
    path('edit/<int:pk>',HabitUpdateAPIView.as_view(),name='habit_update'),
    path('delete/<int:pk>',HabitDestroyAPIView.as_view(),name='habit_delete'),
]