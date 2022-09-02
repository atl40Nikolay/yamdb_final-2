from datetime import date

from django.core.validators import RegexValidator
from rest_framework.exceptions import ValidationError


def validate_date(year):
    current_year = int(date.today().year)
    if year > current_year or year <= 0:
        raise ValidationError('Ошибка! Введен неверный год!')


username_validator = RegexValidator(
    regex=r'^(?!me$)^[\w.@+-]+$',
    message=(
        "Username должен содержать только буквы, "
        "цифры и символы: '@', '.', '+', '-', '_'"
        "и не me"
    )
)
