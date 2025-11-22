from django.contrib.auth.models import AbstractUser
from django.db import models

#Добавляет доп поле
class MyUser(AbstractUser):
    bio = models.TextField('Биография', blank=True)