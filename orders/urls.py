from django.urls import path
from . import views



app_name = 'orders'
urlpatterns = [
    path('add-to-cart/<int:book_id>', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart_view/', views.CartView.as_view(), name='cart_view')
]