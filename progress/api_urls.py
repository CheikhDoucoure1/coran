from rest_framework import viewsets, permissions, serializers
from .models import ProgressionMemorisation, SessionRecitation, BulletinCoranSenegal


class ProgressionSerializer(serializers.ModelSerializer):
    surah_nom = serializers.CharField(source='surah.nom_translittere', read_only=True)
    pourcentage = serializers.ReadOnlyField()

    class Meta:
        model = ProgressionMemorisation
        fields = '__all__'
        read_only_fields = ['eleve']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionRecitation
        fields = '__all__'
        read_only_fields = ['evaluateur', 'date_session']


class BulletinSerializer(serializers.ModelSerializer):
    moyenne_generale = serializers.ReadOnlyField()

    class Meta:
        model = BulletinCoranSenegal
        fields = '__all__'


class ProgressionViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'eleve':
            return ProgressionMemorisation.objects.filter(eleve=user).select_related('surah')
        return ProgressionMemorisation.objects.select_related('eleve', 'surah').all()

    def perform_create(self, serializer):
        serializer.save(eleve=self.request.user)


class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'eleve':
            return SessionRecitation.objects.filter(eleve=user).select_related('surah')
        return SessionRecitation.objects.select_related('eleve', 'surah').all()

    def perform_create(self, serializer):
        serializer.save(evaluateur=self.request.user)


class BulletinViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BulletinSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'eleve':
            return BulletinCoranSenegal.objects.filter(eleve=user)
        return BulletinCoranSenegal.objects.select_related('eleve', 'classe').all()
