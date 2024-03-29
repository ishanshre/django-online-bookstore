from django.urls import path
from . import views



app_name = 'orders'
urlpatterns = [
    path('add-to-cart/<int:book_id>', views.AddToCartView, name='add_to_cart'),
    path('cart_view/', views.CartView, name='cart_view'),
    path('cart_remove/<int:book_id>', views.CartRemove, name='cart_remove'),
    # path('cart_manage_view/<int:cart_item_id>/', views.CartManageView.as_view(), name='cart_manage_view'),
    path('cart_empty_view/', views.CartEmptyView.as_view(), name='cart_empty_view'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('shipping_address/<slug:slug>/', views.ShippingAddressDetailView.as_view(), name='shipping_address_detail'),
    path('order_detail/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
]