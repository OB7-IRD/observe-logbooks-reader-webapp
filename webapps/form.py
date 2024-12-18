from django.contrib.auth.forms import UserCreationForm
from .models import LTOUser
from django.core.exceptions import ValidationError


class LTOUserForm(UserCreationForm):
    class Meta:
        model = LTOUser
        fields = [
            "firstname",
            "lastname",
            "email",
            "username",
            "password1",
            "password2",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if LTOUser.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if LTOUser.objects.filter(email=email).exists():
            raise ValidationError("Cet email est déjà utilisé. Veuillez en fournir un autre.")
        return email