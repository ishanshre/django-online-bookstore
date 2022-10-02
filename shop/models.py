from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.contrib.auth import get_user_model
# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(is_active=True)


class Genre(models.Model):
    genre =  models.CharField(max_length=50)

    def __str__(self):
        return self.genre

class Language(models.Model):
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.language

class Address(models.Model):
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.address

class Publisher(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    email = models.EmailField(max_length=50)
    website = models.URLField(max_length=255)
    established = models.DateField(blank=True, null=True)
    address = models.ManyToManyField(Address)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    description = models.CharField(max_length=300)
    avatar = models.ImageField(upload_to='author_avatar', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=False, unique=True)
    #image = models.ImageField(upload_to='book/', default="default_book.png", blank=True, null=True)
    description = models.CharField(max_length=500)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    language = models.ManyToManyField(Language)
    is_active = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    price = models.FloatField(default=0)
    objects = models.Manager()
    published = PublishedManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Review(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='review')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.rating


class BookImages(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images', default='default.png')
    image = models.ImageField(upload_to=r"{book.title}/", blank=True, null=True)

    def __str__(self):
        return self.book.title