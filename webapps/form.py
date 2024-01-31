from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "basename",
            "url",
            "database",
            "ref_language",
            "defaultdomain",
            "defaultprogram",
            "username",
            "password1",
            "password2"
        ]