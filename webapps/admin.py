from django.contrib import admin
from .models import User

# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display = (
        "username",
        "basename",
        "url",
        "database",
        "ref_language",
        "defaultdomain",
        "defaultprogram"
    )
admin.site.register(User, AdminUser)
