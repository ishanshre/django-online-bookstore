from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserLoginForm
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from .models import Profile

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
            return redirect('shop:index')
        return super(UserLoginView, self).dispatch(request, *args, **kwargs)


class UserPasswordChangeView(LoginRequiredMixin,SuccessMessageMixin, PasswordChangeView):
    template_name = 'password_change.html'
    success_message = 'Password Changed Successfully'
    success_url = reverse_lazy('shop:index')

class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_message = 'Reset email sent to your email address'
    success_url = reverse_lazy('shop:index')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Failed! Please Try Again')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('shop:index')
        return super(UserPasswordResetView, self).dispatch(request, *args, **kwargs)


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_message = 'Password Reset Successfull'
    success_url = reverse_lazy('accounts:login')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Failed! Please Try Again')
        return super().form_invalid(form)
        
class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile.html'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class ProfileUpdateView(LoginRequiredMixin, View):
    
