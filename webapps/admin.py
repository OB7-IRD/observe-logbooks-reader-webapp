from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SiteUser, ConnectionProfile

# Configuration de l'administration pour SiteUser
class SiteUserAdmin(UserAdmin):
    model = SiteUser
    list_display = ('username', 'email', 'access_level', 'account_valid', 'is_staff')
    list_filter = ('access_level', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email',)
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('firstname', 'lastname', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Access', {'fields': ('access_level', 'account_valid')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'access_level', 'account_valid'),
        }),
    )

# Ajout des profils de connexion à l'interface d'administration
class ConnectionProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'database_alias', 'url', 'login')
    search_fields = ('name', 'database_alias', 'login')
    filter_horizontal = ('users',)  # Affiche une interface pour ajouter des utilisateurs au profil

# Enregistrement des modèles dans l'administration
admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(ConnectionProfile, ConnectionProfileAdmin)
