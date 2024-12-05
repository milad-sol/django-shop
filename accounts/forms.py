from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name']

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] and cd['confirm_password'] and cd['password'] != cd['confirm_password']:
            raise ValidationError('Passwords do not match')
        return cd['confirm_password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="You can change password using <a href=\"../password/\">this form</a>."
    )

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password', 'last_login']


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(max_length=11)
    full_name = forms.CharField(label='full_name')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_is_exist = User.objects.filter(email=email).exists()
        if email_is_exist:
            raise ValidationError('Email already exists')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_is_exist = User.objects.filter(phone_number=phone_number).exists()
        if phone_is_exist:
            raise ValidationError('Phone number already exists')
        return phone_number

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match')
        return confirm_password


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginPhoneForm(forms.Form):
    phone_number = forms.CharField(max_length=11,label='',widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))

class LoginVerifyCodeForm(forms.Form):
    code = forms.IntegerField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your code'}))

