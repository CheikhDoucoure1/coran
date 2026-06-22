from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Surah, Verset, GlossaireIslamique, Tajweed
from .serializers import (
    SurahListSerializer, SurahDetailSerializer,
    VersetSerializer, TajweedSerializer, GlossaireSerializer
)


class SurahViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Surah.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom_translittere', 'nom_francais', 'nom_arabe']
    ordering_fields = ['numero', 'niveau_difficulte', 'nombre_versets']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SurahDetailSerializer
        return SurahListSerializer

    @action(detail=True, methods=['get'])
    def versets(self, request, pk=None):
        surah = self.get_object()
        versets = surah.versets.all()
        serializer = VersetSerializer(versets, many=True)
        return Response(serializer.data)


class VersetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Verset.objects.select_related('surah').all()
    serializer_class = VersetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['texte_arabe', 'traduction_fr', 'translitteration']


class TajweedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tajweed.objects.all()
    serializer_class = TajweedSerializer


class GlossaireViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GlossaireIslamique.objects.all()
    serializer_class = GlossaireSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['terme_arabe', 'terme_francais', 'terme_wolof', 'definition_fr']
