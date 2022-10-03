from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserLoginForm, CustomUserChangeForm, ProfileForm
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from accounts.token import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
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
    success_message = 'New User Created. Please check you email for account confirmation and activation'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form, *args, **kwargs):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        current_site = get_current_site(self.request)
        subject = 'Activate your Kitabs Pustakalaya Account'
        message = render_to_string('activation_email.html', {
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            subject, message, to=[to_email]
        )
        email.send()
        return super().form_valid(form, *args, **kwargs)


    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Failed To Create user! Try Again')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('shop:index')
        return super(UserSignUpView, self).dispatch(request, *args, **kwargs)

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user=None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            messages.success(self.request, 'Account Activated Successfully!')
            return redirect('accounts:login')
        else:
            messages.warning(self.request, "Invalid Activation Link")
            return redirect('shop:index')

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
    template_name = 'profile_update.html'
    def get(self, request, *args, **kwargs):
        user_form = CustomUserChangeForm(instance = request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        context = {
            'user_form':user_form,
            'profile_form':profile_form
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        user_form = CustomUserChangeForm(request.POST, instance = request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance = request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Updated')
            return redirect('accounts:profile')
        else:
            user_form = CustomUserChangeForm(instance = request.user)
            profile_form = ProfileForm(instance=request.user.profile)
            messages.error(request, 'Failed! Try Again')
        return render(request, self.template_name, {
            'user_form':user_form,
            'profile_form':profile_form
        })
