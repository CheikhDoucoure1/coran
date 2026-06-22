from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Etablissement, Classe


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'email', 'role', 'telephone', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Scolaires', {'fields': ('role', 'telephone', 'photo')}),
    )


@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type_etablissement', 'region', 'departement', 'directeur']
    list_filter = ['type_etablissement', 'region']
    search_fields = ['nom', 'region', 'departement']


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ['nom', 'niveau', 'etablissement', 'enseignant_principal', 'annee_scolaire']
    list_filter = ['niveau', 'annee_scolaire', 'etablissement']
    search_fields = ['nom', 'etablissement__nom']
    filter_horizontal = ['eleves']
