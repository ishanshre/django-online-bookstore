from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django import forms
from .models import Profile
from django.core.exceptions import ValidationError
from datetime import date
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

class DateInput(forms.DateInput):
    input_type = 'date'


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
        widgets = {
            'date_of_birth': DateInput
        }
    
    def clean_date_of_birth(self, *args, **kwargs):
        dateOfbirth = self.cleaned_data.get("date_of_birth")
        if dateOfbirth > date.today():
            raise ValidationError('Invalid Date')
        return dateOfbirth


class CustomPasswordChangeForm(PasswordChangeForm):
    change_password = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = get_user_model()
        fields = ["old_password", "new_password1", "new_password2"]
