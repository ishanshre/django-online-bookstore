from django import forms
from .models import Order, Address

BOOK_QUANTITY_CHOICES = [(i, str(i)) for i in range(1,21)]
class AddCartForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=BOOK_QUANTITY_CHOICES, coerce=int)
    overrides = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class CheckOutForm(forms.ModelForm):
    '''
    shipping address displays all address
    so using init method to display shipping address to users only
    we pass the user from CheckOut Form Create view using get_from_kwargs method
    '''
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shipping_address'].queryset = Address.objects.filter(user=user)
    class Meta:
        model = Order
        fields = ['shipping_address',]


class ShippingAddressForm(forms.ModelForm):
    update_address = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = Address
        fields = ['country', 'province', 'city', 'zip_code', 'street_address' ]

class ShippingAddressDeleteForm(forms.Form):
    delete_address = forms.BooleanField(widget=forms.HiddenInput, initial=True)

