from django import forms
from .models import PasswordEntry
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PasswordEntryForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = PasswordEntry
        fields = ['site_name', 'login', 'password', 'category']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')