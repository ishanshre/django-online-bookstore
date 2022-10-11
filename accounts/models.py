
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(AbstractUser):
    class GENDER(models.TextChoices):
        MALE = "MALE", 'MALE'
        FEMALE = "FEMALE", 'FEMALE'
        OTHERS = "OTHERS", 'OTHERS'


    age = models.PositiveIntegerField(blank = True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER.choices, blank=True, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile_avatar/', blank=True, null=True, default='default.png')
    identity = models.ImageField(upload_to='identity/', blank=True, null=True,  default='default.png')
    date_of_birth = models.DateField(null=True, blank=True)
    phone = PhoneNumberField(blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    created =models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username