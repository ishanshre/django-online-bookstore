from django.db import models


class CITY_CHOICES(models.TextChoices):
    KATHMANDU = "Kathmandu", 'Kathmandu'
    LALITPUR = "Lalitpur", 'Lalitpur'
    BHAKTAPUR = "Bhaktapur", 'Bhaktapur'