from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserLoginForm
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

# Create your views here.


class UserSignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_message = 'New User Created'
    success_url = reverse_lazy('accounts:login')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Failed To Create user! Try Again')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('shop:index')
        return super(UserSignUpView, self).dispatch(request, *args, **kwargs)

class UserLoginView(messages.views.SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'
    success_message = 'User Login Successfull'
    
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Invalid username or password')
        return super().form_invalid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('shop:index.html')
        return super(UserLoginView, self).dispatch(request, *args, **kwargs)
