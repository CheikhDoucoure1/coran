from rest_framework import serializers
from .models import Surah, Verset, GlossaireIslamique, Tajweed


class VersetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verset
        fields = ['id', 'numero', 'texte_arabe', 'translitteration',
                  'traduction_fr', 'traduction_wolof', 'notes_pedagogiques', 'audio_url']


class SurahListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surah
        fields = ['id', 'numero', 'nom_arabe', 'nom_translittere', 'nom_francais',
                  'nombre_versets', 'type_revelation', 'niveau_difficulte']


class SurahDetailSerializer(serializers.ModelSerializer):
    versets = VersetSerializer(many=True, read_only=True)

    class Meta:
        model = Surah
        fields = '__all__'


class TajweedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tajweed
        fields = '__all__'


class GlossaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaireIslamique
        fields = '__all__'
