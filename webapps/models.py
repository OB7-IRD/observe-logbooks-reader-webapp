from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    basename = models.CharField(max_length=200)
    url = models.CharField(max_length=300)
    database = models.CharField(max_length=100)
    ref_language = models.CharField(max_length=50)
    defaultdomain = models.CharField(max_length=50)
    defaultprogram = models.CharField(max_length=200)


