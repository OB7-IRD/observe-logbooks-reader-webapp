from django.forms import ModelForm
from django.forms.widgets import PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import WebServiceUserModel

User = get_user_model()
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "basename",
            "url",
            "database",
            # "ref_language",
            # "defaultdomain",
            # "defaultprogram",
            "username",
            "password",
            # "password2"
        ]


class WSUserModelForm(ModelForm):
    class Meta:
        model = WebServiceUserModel
        fields = [
            "basename",
            "url",
            "database",
            "username",
            "password",
            ]

        widgets = {
            "password": PasswordInput()
        }