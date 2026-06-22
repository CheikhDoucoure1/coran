from django.contrib import admin
from .models import NiveauScolaire, ProgrammeCoranSenegal, SourateParNiveau, PlanDeLecon, Ressource


@admin.register(NiveauScolaire)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'cycle', 'ordre']
    list_filter = ['cycle']
    ordering = ['ordre']


class SourateParNiveauInline(admin.TabularInline):
    model = SourateParNiveau
    extra = 1
    fields = ['surah', 'periode', 'versets_debut', 'versets_fin', 'obligatoire', 'ordre_enseignement']


@admin.register(ProgrammeCoranSenegal)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ['niveau', 'heures_hebdomadaires', 'annee_scolaire']
    inlines = [SourateParNiveauInline]


@admin.register(PlanDeLecon)
class PlanDeLeconAdmin(admin.ModelAdmin):
    list_display = ['titre', 'niveau', 'surah', 'duree_minutes', 'auteur', 'statut', 'date_creation']
    list_filter = ['statut', 'niveau', 'surah']
    search_fields = ['titre', 'objectifs']
    raw_id_fields = ['surah', 'auteur']
    date_hierarchy = 'date_creation'


@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_ressource', 'surah', 'date_ajout']
    list_filter = ['type_ressource']
    search_fields = ['titre', 'description']
