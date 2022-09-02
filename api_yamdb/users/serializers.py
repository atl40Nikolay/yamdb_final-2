from rest_framework import serializers

from .models import CustomUser
from .role_enums import Roles


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = CustomUser


class ConfCodeSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = CustomUser


class AdminCreateUser(serializers.ModelSerializer):
    role = serializers.ChoiceField(default='user', choices=Roles.choices())

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
