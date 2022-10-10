from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django import forms
from .models import Profile
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username','email']


class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','age','gender','username','email']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)


    class Meta:
        model  = get_user_model()
        fields = ['username', 'password','remember_me']


class ProfileForm(forms.ModelForm):
    profile_update = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = Profile
        fields = [
            'avatar',
            'identity',
            'date_of_birth',
            'phone',
        ]

class CustomPasswordChangeForm(PasswordChangeForm):
    change_password = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = get_user_model()
        fields = ["old_password", "new_password1", "new_password2"]
