from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Modèle pour les utilisateurs du site
class LTOUser(AbstractUser):
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    email = models.EmailField(max_length=128, unique=True)
    username = models.CharField(max_length=54, unique=True)
    password = models.CharField(max_length=128)  # Django gère le hachage du mot de passe
    account_valid = models.BooleanField(default=False)  # Contrôlé par l'administrateur
    access_level = models.CharField(
        max_length=20,
        choices=[('user', 'Users'), ('admin', 'Administrators')],
        default='user'
    )

    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.access_level}"


# Modèle pour les profils de connexion créés par l'administrateur
class ConnectionProfile(models.Model):
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=512)
    login = models.CharField(max_length=64)
    password = models.CharField(max_length=64)  # Stocké en clair pour une utilisation dans la page d'administration
    database_alias = models.CharField(max_length=64)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="connection_profiles", blank=True)  # vide au départ

    def __str__(self):
        return f"{self.name} - {self.database_alias}"  # Affiche un nom plus lisible
