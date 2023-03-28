from django.shortcuts import render, redirect
from .forms import ContactForm
from django.views import View
from django.contrib import messages
#from orders.views import CartMixin
# Create your views here.

class ContactUs(View):
    template_name = 'contact/contact_us.html'
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {'form':form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully')
            return redirect('shop:index')
        else:
            form = ContactForm()
            messages.error(request, 'Failed! Please try again')
        return render(request, self.template_name, {'form':form})
            
