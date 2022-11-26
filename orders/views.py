from django.shortcuts import render, redirect, get_object_or_404
from orders.cart import Cart
from shop.models import Book
from orders.models import Order, Address, OrderItem
from django.views import View
from orders.forms import AddCartForm, CheckOutForm, ShippingAddressDeleteForm, ShippingAddressForm
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages


@require_POST
def AddToCartView(request, book_id):
    cart = Cart(request=request)
    book = get_object_or_404(Book, id=book_id)
    form = AddCartForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data # cd -> cleaned_data ---> minimizing the code
        cart.add(book=book, quantity=cd['quantity'], overrides_quantity = cd['overrides'])
    return redirect("orders:cart_view")


def CartView(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = AddCartForm(initial={
            'quantity':item['quantity'],
            'override':True
        })
    return render(request, "cart_view.html", {"cart":cart})

@require_POST
def CartRemove(request, book_id):
    cart = Cart(request)
    cart.remove(book_id)
    return redirect("orders:cart_view")
class CartEmptyView(View):
    pass

class CheckoutView(LoginRequiredMixin, CreateView):
    template_name: str = "checkout.html"
    form_class = CheckOutForm
    success_url = "orders:order_detail"

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context
    
    def form_valid(self, form):
        form.instance.ordered_by = self.request.user
        order = form.save()
        cart = Cart(self.request)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                book = item['book'],
                price = item['price'],
                quantity = item['quantity'],
            )
        cart.delete_session()
        messages.success(self.request, "Checkout Successfull")
        return redirect("accounts:profile_and_update")
        return super().form_valid(form)


class OrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'order_detail.html'

    def get_queryset(self):
        return Order.objects.filter(ordered_by=self.request.user)


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
        shipping_address = Address.objects.get(slug=address_slug)
        if 'update_address' in request.POST:
            update_form = ShippingAddressForm(request.POST, instance=shipping_address)
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
                shipping_address.delete()
                messages.success(request, "Shipping Address Deleted Successfull")
                return redirect("accounts:profile_and_update")
            else:
                messages.error(request, "Detete Failed! Please Try Again")
                return redirect('orders:shipping_address_detail', address_slug)
        context = {
            'shipping_address': shipping_address,
            'update_form':update_form,
            'delete_form':delete_form,
        }
        return render(request, self.template_name, context)
    
    def test_func(self):
        address = Address.objects.get(slug=self.kwargs['slug'])
        return address.user == self.request.user