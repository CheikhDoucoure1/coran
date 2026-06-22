from django.contrib import admin
from .models import Surah, Verset, Tajweed, GlossaireIslamique


class VersetInline(admin.TabularInline):
    model = Verset
    extra = 0
    fields = ['numero', 'texte_arabe', 'traduction_fr', 'translitteration']
    show_change_link = True


@admin.register(Surah)
class SurahAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nom_arabe', 'nom_translittere', 'nom_francais',
                    'nombre_versets', 'type_revelation', 'niveau_difficulte']
    list_filter = ['type_revelation', 'niveau_difficulte']
    search_fields = ['nom_arabe', 'nom_translittere', 'nom_francais']
    ordering = ['numero']
    inlines = [VersetInline]


@admin.register(Verset)
class VersetAdmin(admin.ModelAdmin):
    list_display = ['surah', 'numero', 'texte_arabe']
    list_filter = ['surah']
    search_fields = ['texte_arabe', 'traduction_fr', 'translitteration']
    raw_id_fields = ['surah']


@admin.register(Tajweed)
class TajweedAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'niveau_scolaire']
    list_filter = ['categorie']
    search_fields = ['nom', 'description_fr']


@admin.register(GlossaireIslamique)
class GlossaireAdmin(admin.ModelAdmin):
    list_display = ['terme_arabe', 'terme_francais', 'terme_wolof']
    search_fields = ['terme_arabe', 'terme_francais', 'definition_fr']
