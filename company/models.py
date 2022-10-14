from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor_uploader.fields import RichTextUploadingField 
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext as _
from django.utils.text import slugify
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextUploadingField(max_length=1000)
    email = models.EmailField()
    website = models.URLField()
    address = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company/logo', null=True, blank=True)
    logo_name = models.CharField(max_length=50, null=True, blank=True)
    main_banner_image = models.ImageField(upload_to='company/MainBannerImage')
    main_banner_name = models.CharField(max_length=50, null=True, blank=True)
    main_banner_quote = models.CharField(max_length=100, null=True, blank=True)
    main_banner_link = models.CharField(max_length=100, null=True, blank=True)
    terms_and_conditions = models.CharField(max_length=20000, null=True, blank=True)
    slug = AutoSlugField(_('slug'), max_length=100, unique=True, populate_from=('name',))
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
class CompanyPhoneNumber(models.Model):
    phone = PhoneNumberField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_phone')

    def __str__(self):
        return str(self.phone)

class Achievement(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='company/achievement', null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_achievement')
    slug = AutoSlugField(_('slug'), max_length=50, unique=True, populate_from=('title',))
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=100, null=True, blank=True)
    answer = models.CharField(max_length=1000, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_faq')

    def __str__(self):
        return self.question

class Carrer(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=5000, null=True, blank=True)
    full_time = models.BooleanField(default=True)
    part_time = models.BooleanField(default=False)
    remote_time = models.BooleanField(default=False)
    slug = AutoSlugField(_('slug'), max_length=50, unique=True, populate_from=('title',))
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class CV(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = phone = PhoneNumberField(blank=True, null=True)
    address = models.CharField(max_length=200)
    resume = models.FileField(upload_to='company/resume/')
    carrer = models.ForeignKey(Carrer, on_delete=models.SET_NULL, related_name='carrer_cv', null=True)
