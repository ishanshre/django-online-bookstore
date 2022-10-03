from django.db import models

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    phone = models.PositiveIntegerField(max_length=10)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=500)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"