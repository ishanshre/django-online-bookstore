from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from shop.models import Book
from .models import Cart,CartItem
from django.contrib import messages
# Create your views here.
class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        #get product id
        book_id = self.kwargs['book_id']
        #get product
        book_object = Book.objects.get(id=book_id)
        #check if cart exist 
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            items_in_cart = cart.cartitems.filter(book=book_object)
            if items_in_cart.exists():
                cart_item = items_in_cart.last()
                cart_item.quantity += 1
                cart_item.subtotal += book_object.price
                cart_item.save()
                cart.total += book_object.price
                cart.save()
                messages.success(request, 'Item Added To Cart')
                return redirect('shop:index')
            else:
                cart_item = CartItem.objects.create(
                    cart = cart,
                    book = book_object,
                    rate = book_object.price,
                    quantity=1,
                    subtotal=book_object.price
                )
                cart.total += book_object.price
                cart.save()
                messages.success(request, 'Item Added To Cart')
                return redirect('shop:index')
        else:
            cart_object = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_object.id
            cart_item = CartItem.objects.create(
                    cart = cart,
                    book = book_object,
                    rate = book_object.price,
                    quantity=1,
                    subtotal=book_object.price
                )
            cart.total += book_object.price
            cart.save()
            messages.success(request, 'Item Added To Cart')
            return redirect('shop:index')
        #check if cart product already in cart

        return redirect('shop:index')


class CartView(TemplateView):
    template_name = 'cart_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart 
        return context
               