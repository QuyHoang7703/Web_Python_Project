from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
class CreateFormRegister(UserCreationForm):
    name = forms.CharField(max_length=255, required=True)
    address = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "name", "address", "phone", "email"]

            
class CreateLoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password"]
    