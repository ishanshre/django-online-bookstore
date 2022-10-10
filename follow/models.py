from django.db import models
from shop.models import Author
from django.contrib.auth import get_user_model
# Create your models here.


class Follow(models.Model):
    followed_by = models.ForeignKey(get_user_model(), related_name="user_follows", on_delete=models.CASCADE)
    followed = models.ForeignKey(Author, related_name='user_followers', on_delete=models.CASCADE)
    muted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.followed_by.username} follows {self.followed.first_name} {self.followed.last_name}"
