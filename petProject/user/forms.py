from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Account


class SignUpForm(UserCreationForm):
    class Meta:
        model = Account
        fields = [
            "name",
            "username",
            "email",
            "breed",
            "animal",
            "bio",
            "date_of_birth",
            "password1",
            "password2",
        ]


class SignUpEditForm(ModelForm):
    class Meta:
        model = Account
        fields = [
            "name",
            "username",
            "email",
            "breed",
            "animal",
            "bio",
            "date_of_birth",
        ]
