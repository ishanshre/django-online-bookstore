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
                    cart = cart_object,
                    book = book_object,
                    rate = book_object.price,
                    quantity=1,
                    subtotal=book_object.price
                )
            cart_object.total += book_object.price
            cart_object.save()
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


class CartManageView(View):
    def get(self, request, *args, **kwargs):
        cart_item_id = self.kwargs['cart_item_id']
        action = request.GET.get('action')
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart = cart_item.cart
        if action == 'inc':
            cart_item.quantity += 1
            cart_item.subtotal += cart_item.rate
            cart_item.save()
            cart.total += cart_item.rate
            cart.save()
        elif action == 'dec':
            cart_item.quantity -= 1
            cart_item.subtotal -= cart_item.rate
            cart_item.save()
            cart.total -= cart_item.rate
            cart.save()
            if cart_item.quantity == 0:
                cart_item.delete()

        elif action == 'rem':
            cart.total -= cart_item.subtotal
            cart.save()
            cart_item.delete()
        else:
            pass
        return redirect('orders:cart_view')


class CartEmptyView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartitems.all().delete()
            cart.total = 0
            cart.save()
        return redirect("orders:cart_view")
