from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User
from users.validators import validate_unique_email


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'avatar', 'telegram_id', 'telegram_nik', 'password', 'id']
        validators = [validate_unique_email]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
