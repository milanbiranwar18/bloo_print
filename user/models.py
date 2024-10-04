from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    mobile_num = models.IntegerField()
    location = models.CharField(max_length=100)
