from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from core.validators import username_validator
from .role_enums import Roles


class CustomUser(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[username_validator],
        blank=False,
    )
    email = models.EmailField(max_length=254,
                              unique=True,
                              blank=False
                              )
    first_name = models.CharField(max_length=150,
                                  blank=True
                                  )
    last_name = models.CharField(max_length=150,
                                 blank=True
                                 )
    bio = models.TextField(blank=True)
    role = models.CharField(choices=Roles.choices(),
                            default='user',
                            max_length=Roles.max_len()
                            )
    # confirmation_code = models.CharField(max_length=36, blank=True)

    def get_tokens_for_user(self):
        refresh = RefreshToken.for_user(self)
        return {'access': str(refresh.access_token)}

    @property
    def is_admin(self):
        return self.role == Roles.ADMIN.name.lower()

    @property
    def is_moderator(self):
        return self.role == Roles.MODERATOR.name.lower()

    @property
    def is_user(self):
        return self.role == Roles.USER.name.lower()

    def __str__(self):
        return self.email
