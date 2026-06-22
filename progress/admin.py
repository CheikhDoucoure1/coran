from django.contrib import admin
from .models import ProgressionMemorisation, SessionRecitation, BulletinCoranSenegal


@admin.register(ProgressionMemorisation)
class ProgressionAdmin(admin.ModelAdmin):
    list_display = ['eleve', 'surah', 'statut', 'versets_memorises', 'note_recitation', 'derniere_evaluation']
    list_filter = ['statut', 'surah']
    search_fields = ['eleve__username', 'eleve__last_name', 'surah__nom_translittere']
    raw_id_fields = ['eleve', 'surah']


@admin.register(SessionRecitation)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['eleve', 'surah', 'note', 'evaluation_qualitative', 'evaluateur', 'date_session']
    list_filter = ['evaluation_qualitative', 'surah', 'tajweed_respecte']
    search_fields = ['eleve__username', 'eleve__last_name']
    date_hierarchy = 'date_session'
    raw_id_fields = ['eleve', 'evaluateur']


@admin.register(BulletinCoranSenegal)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ['eleve', 'classe', 'periode', 'annee_scolaire',
                    'note_memorisation', 'note_recitation', 'note_tajweed']
    list_filter = ['periode', 'annee_scolaire', 'classe']
    search_fields = ['eleve__username', 'eleve__last_name']
    filter_horizontal = ['sourates_validees']
