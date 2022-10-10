from django.db import models
from shop.models import Book
from django.contrib.auth import get_user_model
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='users', null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart: {str(self.id)}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='cartbooks')
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return f"Cart: {str(self.cart.id)} Cart Product: {str(self.id)}"
