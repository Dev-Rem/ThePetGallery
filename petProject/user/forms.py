from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Account


class SignUpForm(UserCreationForm):
    class Meta:
        model = Account
        fields = [
            "name",
            "username",
            "email",
            "password1",
            "password2",
        ]
