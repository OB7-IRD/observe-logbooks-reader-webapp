from django.db.models.signals import post_migrate, post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import LTOUser

@receiver(post_save, sender=LTOUser)
def create_groups_and_assign_user(sender, instance, created, **kwargs):
    # Vérifier si un utilisateur vient d'être créé
    if created:
        # Ajouter l'utilisateur au groupe "Users"
        user_group, _ = Group.objects.get_or_create(name='Users')
        instance.groups.add(user_group)  # Ajouter au groupe

    # Créer les groupes "Users" et "Administrators" s'ils n'existent pas
    Group.objects.get_or_create(name='Users')
    Group.objects.get_or_create(name='Administrators')


@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    """ Crée un utilisateur admin par défaut après les migrations """
    User = get_user_model()

    # Vérifier si l'utilisateur admin par défaut existe déjà
    if not User.objects.filter(username="admin").exists():
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="changeme",
            firstname="Admin",
            lastname="Default",
            account_valid=True,
            access_level="admin"
        )

        # Ajouter l'utilisateur admin au groupe des administrateurs
        admin_group, _ = Group.objects.get_or_create(name="Administrators")
        admin_user.groups.add(admin_group)
        admin_user.save()
        print("Administrateur par défaut créé avec succès.")
