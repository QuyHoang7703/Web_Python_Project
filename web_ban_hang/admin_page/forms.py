from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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


class CreateUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=255, required=True)
    address = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'address', 'phone']
        # 'username' field is already included in UserChangeForm

    def __init__(self, *args, **kwargs):
        super(CreateUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True  # Disable the username field

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

