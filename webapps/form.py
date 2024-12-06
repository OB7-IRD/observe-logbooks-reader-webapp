from django.contrib.auth.forms import UserCreationForm
from .models import SiteUser
from django.core.exceptions import ValidationError


class SiteUserForm(UserCreationForm):
    class Meta:
        model = SiteUser
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
        if SiteUser.objects.filter(username=username).exists():
            raise ValidationError("Ce non d'utilisateur est déjà pris. Veuillez en choisir un autre.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if SiteUser.objects.filter(email=email).exists():
            raise ValidationError("Cet email est déjà utilisé. Veuillez en fournir un autre.")
        return email