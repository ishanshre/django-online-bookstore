from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django import forms
from .models import Profile
from django.core.exceptions import ValidationError
from datetime import date
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username','email']
    
    def clean_email(self):
        User = get_user_model()
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email is already in use')
        return data


class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','age','gender','username','email']
    
    def clean_email(self):
        User = get_user_model()
        data = self.cleaned_data['email']
        query = User.objects.exclude(id = self.instance.id).filter(email=data)
        if query.exists():
            raise forms.ValidationError('Email is already in use')
        return data

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
            'date_of_birth': DateInput,
            'phone': PhoneNumberPrefixWidget(initial="NP")
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
