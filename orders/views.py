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

class CartMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            try:
                cart = Cart.objects.get(id = cart_id)
                if request.user.is_authenticated:
                    cart.user = request.user
                    cart.save()
            except:
                pass
        return super().dispatch(request, *args, **kwargs)



class AddToCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        #get product id
        book_id = self.kwargs['book_id']
        #get product
        book_object = Book.objects.get(id=book_id)
        #check if cart exist 
        if self.request.user.is_authenticated:
            exist_cart = request.user.users.last()
            if exist_cart:
                cart_id = exist_cart.id
                if cart_id:
                    cart = exist_cart
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
                cart_object = Cart.objects.create(total=0, user=request.user)
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
        else:
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


class CartView(CartMixin, TemplateView):
    template_name = 'cart_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            exist_cart = self.request.user.users.last()
            if exist_cart:
                cart = exist_cart
            else:
                cart_id = self.request.session.get('cart_id', None)
                cart = None
                if cart_id:
                    try:
                        cart = Cart.objects.get(id=cart_id)
                    except:
                        cart = None
        else:
            cart_id = self.request.session.get('cart_id', None)
            cart = None
            if cart_id:
                try:
                    cart = Cart.objects.get(id=cart_id)
                except:
                    cart = None
        context['cart'] = cart 
        return context


class CartManageView(CartMixin, View):
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


class CartEmptyView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            exist_cart = request.user.users.last()
            if exist_cart:
                cart_id = exist_cart.id
                if cart_id:
                    cart = exist_cart
                    cart.cartitems.all().delete()
                    cart.total = 0
                    cart.save()
                return redirect("orders:cart_view")
            else:
                cart_id = request.session.get('cart_id', None)
                if cart_id:
                    cart = Cart.objects.get(id=cart_id)
                    cart.cartitems.all().delete()
                    cart.total = 0
                    cart.save()
                return redirect("orders:cart_view")
        else:
            cart_id = request.session.get('cart_id', None)
            if cart_id:
                cart = Cart.objects.get(id=cart_id)
                cart.cartitems.all().delete()
                cart.total = 0
                cart.save()
            return redirect("orders:cart_view")
        return redirect("orders:cart_view")

class CheckoutView(LoginRequiredMixin, CartMixin, CreateView):
    template_name = 'checkout.html'
    form_class = CheckOutForm
    success_url = reverse_lazy('shop:index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        exist_cart = self.request.user.users.last()
        if exist_cart:
            cart_id = exist_cart.id
            cart = None
            if cart_id:
                cart = exist_cart
        else:
            cart_id = self.request.session.get('cart_id', None)
            cart = None
            if cart_id:
                cart = Cart.objects.get(id=cart_id)
        context['cart'] = cart
        return context
    '''
    Using get_from_kwargs method we pass the logged in user to the checkout form
    '''
    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        exist_cart = self.request.user.users.last()
        if exist_cart:
            cart = exist_cart
            form.instance.cart = cart
            form.instance.ordered_by = self.request.user
            form.instance.subtotal = cart.total
            form.instance.discount = 0
            form.instance.total = cart.total
            form.instance.order_status = "Order Received"
            form.instance.save()
            #now linking cartitems order to order model
            for items in cart.cartitems.all():
                items.order = form.instance
                items.save()
            session_id =  self.request.session.get('cart_id')
            del session_id # deleting cart session
            exist_cart.delete() # deleting existing cart
            messages.success(self.request, 'Checkout Successfull')
            return redirect('shop:index')
        else:
            return redirect('shop:index')
        # else:
        #     cart_id = self.request.session.get("cart_id", None)
        #     if cart_id:
        #         cart = Cart.objects.get(id=cart_id)
        #         form.instance.cart = cart
        #         form.instance.ordered_by = self.request.user
        #         form.instance.subtotal = cart.total
        #         form.instance.discount = 0
        #         form.instance.total = cart.total
        #         form.instance.order_status = "Order Received"
        #         del self.request.session['cart_id']
        #         messages.success(self.request, 'Checkout Successfull')
        #     else:
        #         return redirect("shop:index")
       


class ShippingAddressDetailView(LoginRequiredMixin,UserPassesTestMixin, CartMixin, View):
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