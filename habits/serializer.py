from rest_framework import serializers
from habits.models import Habits
from habits.validators import TimeCompleteValidator, ChoiceValidator, RelatedPleasantValidator, PleasantValidator, \
    PeriodicityValidator


class HabitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = '__all__'
        validators = [
            TimeCompleteValidator(field='time_to_complete'),
            ChoiceValidator(field1='related_habit', field2='reward'),
            RelatedPleasantValidator(field1='related_habit', field2='is_pleasant_habit'),
            PleasantValidator(field1='is_pleasant_habit', field2='reward', field3='related_habit'),
            PeriodicityValidator(field='periodicity')
        ]
