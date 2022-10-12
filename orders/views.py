from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from shop.models import Book
from .models import Cart,CartItem, Address
from .forms import CheckOutForm, ShippingAddressForm, ShippingAddressDeleteForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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


class CheckoutView(LoginRequiredMixin, CreateView):
    template_name = 'checkout.html'
    form_class = CheckOutForm
    success_url = reverse_lazy('shop:index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_id = self.request.session.get('cart_id', None)
        cart = None
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        context['cart'] = cart
        return context
    
    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            form.instance.cart = cart
            form.instance.ordered_by = self.request.user
            form.instance.subtotal = cart.total
            form.instance.discount = 0
            form.instance.total = cart.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
            messages.success(self.request, 'Checkout Successfull')
        else:
            return redirect("shop:index")
        return super().form_valid(form)

class ShippingAddressDetailView(LoginRequiredMixin,UserPassesTestMixin, View):
    template_name = 'shipping_address.html'
    def get(self, request, *args, **kwargs):
        address_slug = self.kwargs['slug']
        shipping_address = Address.objects.get(slug=address_slug)
        update_form = ShippingAddressForm(instance=shipping_address)
        delete_form = ShippingAddressDeleteForm()
        context = {
            'shipping_address': shipping_address,
            'update_form':update_form,
            'delete_form':delete_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        address_slug = self.kwargs['slug']
        address_instance = Address.objects.get(slug=address_slug)
        if 'update_address' in request.POST:
            update_form = ShippingAddressForm(request.POST, instance=address_instance)
            if update_form.is_valid():
                a = update_form.save()
                messages.success(request, "Shipping address updated")
                return redirect('orders:shipping_address_detail', a.slug)
            else:
                messages.error(request, "Failed to update! Please try again")
                return redirect('orders:shipping_address_detail', address_slug)
        if 'delete_address' in request.POST:
            delete_form = ShippingAddressDeleteForm(request.POST)
            if delete_form.is_valid():
                address_instance.delete()
                messages.success(request, "Shipping Address Deleted Successfull")
                return redirect("accounts:profile_and_update")
            else:
                messages.error(request, "Detete Failed! Please Try Again")
                return redirect('orders:shipping_address_detail', address_slug)
        context = {
            'form':form,
        }
        return render(request, self.template_name, context)
    
    def test_func(self):
        address = Address.objects.get(slug=self.kwargs['slug'])
        return address.user == self.request.user