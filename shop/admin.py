from django.contrib import admin
from .models import (
    Genre,
    Language,
    Address,
    Publisher,
    Author,
    Book,
    Review,
    BookImages
)
# Register your models here.

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Address)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookImages)