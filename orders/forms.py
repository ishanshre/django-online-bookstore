from django import forms
from .models import Order, Address



class CheckOutForm(forms.ModelForm):
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