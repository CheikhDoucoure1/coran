from rest_framework import viewsets
from .models import NiveauScolaire, ProgrammeCoranSenegal, PlanDeLecon
from .serializers import NiveauScolaireSerializer, ProgrammeSerializer, PlanDeLeconSerializer


class NiveauViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NiveauScolaire.objects.all()
    serializer_class = NiveauScolaireSerializer


class ProgrammeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProgrammeCoranSenegal.objects.select_related('niveau').all()
    serializer_class = ProgrammeSerializer


class PlanDeLeconViewSet(viewsets.ModelViewSet):
    queryset = PlanDeLecon.objects.filter(statut='valide').select_related('niveau', 'surah')
    serializer_class = PlanDeLeconSerializer

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)
