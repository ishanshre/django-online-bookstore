from django.contrib import admin
from .models import OrderItem, Order, Address
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
