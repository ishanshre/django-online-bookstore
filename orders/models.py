from django.db import models
from shop.models import Book
from django.contrib.auth import get_user_model
from .Nepal import CITY_CHOICES, PROVINCE_CHOICES
from .countries import COUNTRIES_CHOOSE
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='users', null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart: {str(self.id)}"



class Address(models.Model):
    class ADDRESS_TYPE(models.TextChoices):
        SHIPPING_ADDRESS = "Shipping Address", 'Shipping Address'
        BILLING_ADDRESS = "Billing Address", 'Billing Address'
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="order_address")
    street_address = models.CharField(max_length=100)
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES.choices, default=PROVINCE_CHOICES.BAGMATI)
    city = models.CharField(max_length=20, choices=CITY_CHOICES.choices, default=CITY_CHOICES.KATHMANDU)
    country = models.CharField(max_length=50, choices=COUNTRIES_CHOOSE.choices, default=COUNTRIES_CHOOSE.Nepal)
    zip_code = models.CharField(max_length=50)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE.choices, default=ADDRESS_TYPE.SHIPPING_ADDRESS)
    default = models.BooleanField(default=False)
    slug = AutoSlugField(_('slug'), max_length=100, unique=True, populate_from=('user.username','street_address','province',), editable=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username+' '+self.street_address+' '+self.province)
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.street_address

    def get_absolute_url(self):
        return reverse('orders:shipping_address_detail', args=[self.slug])


class Order(models.Model):
    class ORDER_STATUS(models.TextChoices):
        ORDER_RECEIVED = "Order Received", 'Order Received'
        ORDER_PROCESSING = "Order Processing", 'Order Processing'
        ON_THE_WAY = "On The Way", 'On The Way' 
        ORDER_COMPLETED = "Order Completed", 'Order Completed'
        ORDER_CANCELED = "Order Canceled", 'Order Canceled'
    

    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, related_name='order_placed', null=True, blank=True)
    ordered_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL, null=True, blank=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL, null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS.choices)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Order: {str(self.id)}"

    def get_absolute_url(self):
        return reverse('orders:order_detail', kwargs={'pk':self.pk})

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, related_name='cartitems', null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems', null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='cartbooks')
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return f"Book: {self.book.title}"