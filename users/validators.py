from rest_framework.serializers import ValidationError
from users.models import User


def validate_unique_email(value):
    """
    Проверяет, что email уникален в базе данных.
    """
    if User.objects.filter(email=value).exists():
        raise ValidationError("Пользователь с такой почтой уже существует")
