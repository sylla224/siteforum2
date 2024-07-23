from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


# Create your models here.
class ForumUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=240, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
