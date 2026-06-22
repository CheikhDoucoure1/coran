from rest_framework import serializers
from .models import NiveauScolaire, ProgrammeCoranSenegal, PlanDeLecon, SourateParNiveau


class NiveauScolaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = NiveauScolaire
        fields = '__all__'


class SourateParNiveauSerializer(serializers.ModelSerializer):
    surah_nom = serializers.CharField(source='surah.nom_translittere', read_only=True)
    surah_numero = serializers.IntegerField(source='surah.numero', read_only=True)

    class Meta:
        model = SourateParNiveau
        fields = '__all__'


class ProgrammeSerializer(serializers.ModelSerializer):
    niveau = NiveauScolaireSerializer(read_only=True)
    sourates = SourateParNiveauSerializer(source='sourateniveau_set', many=True, read_only=True)

    class Meta:
        model = ProgrammeCoranSenegal
        fields = '__all__'


class PlanDeLeconSerializer(serializers.ModelSerializer):
    niveau_nom = serializers.CharField(source='niveau.nom', read_only=True)
    surah_nom = serializers.CharField(source='surah.nom_translittere', read_only=True)

    class Meta:
        model = PlanDeLecon
        fields = '__all__'
        read_only_fields = ['auteur', 'date_creation', 'date_modification']
