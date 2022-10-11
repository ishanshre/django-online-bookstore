from django.db import models


class PROVINCE_CHOICES(models.TextChoices):
    PROVINCE1 = "Province 1", 'Province 1'
    MADHESH = "Madhesh", 'Madhesh'
    BAGMATI = "Bagmati", 'Bagmati'
    GANDAKI = "Gandaki", 'Gandaki'
    LUMBINI = "Lumbini", 'Lumbini'
    KARNALI = "Karnali", 'Karnali'
    SUDURPASHCHIM = "Sudurpashchim", 'Sudurpashchim'


class CITY_CHOICES(models.TextChoices):
    KATHMANDU = "Kathmandu", 'Kathmandu'
    LALITPUR = "Lalitpur", 'Lalitpur'
    BHAKTAPUR = "Bhaktapur", 'Bhaktapur'