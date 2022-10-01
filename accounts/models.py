
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    class GENDER(models.TextChoices):
        MALE = "MALE", 'MALE'
        FEMALE = "FEMALE", 'FEMALE'
        OTHERS = "OTHERS", 'OTHERS'


    age = models.PositiveIntegerField(blank = True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER.choices, blank=True, null=True)
