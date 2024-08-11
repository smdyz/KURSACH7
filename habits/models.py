from django.conf import settings
from django.db import models

from users.models import NULLABLE


class Habits(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='создатель привычки')
    place = models.CharField(max_length=200, verbose_name='место,в котором необходимо выполнять привычку')
    time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='время, когда необходимо выполнять привычку')
    action = models.CharField(max_length=300, verbose_name='привычка')
    is_pleasant_habit = models.BooleanField(default=True, verbose_name='признак приятной привычки', **NULLABLE)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='связанная привычка')
    periodicity = models.IntegerField(default=1, verbose_name='периодичность выполнения привычки в неделю')
    reward = models.CharField(max_length=100, null=True, blank=True, verbose_name='вознаграждение')
    time_to_complete = models.IntegerField(verbose_name='время на выполнение')
    is_public = models.BooleanField(default=True, verbose_name='признак публичности')

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
