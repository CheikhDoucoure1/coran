from rest_framework import viewsets, permissions, serializers
from .models import Quiz, TentativeQuiz


class QuizSerializer(serializers.ModelSerializer):
    nb_questions = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['createur']

    def get_nb_questions(self, obj):
        return obj.questions.count()


class TentativeSerializer(serializers.ModelSerializer):
    pourcentage_reussite = serializers.ReadOnlyField()

    class Meta:
        model = TentativeQuiz
        fields = '__all__'
        read_only_fields = ['eleve', 'date_debut']


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.filter(actif=True).select_related('niveau', 'surah')
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(createur=self.request.user)


class TentativeViewSet(viewsets.ModelViewSet):
    serializer_class = TentativeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TentativeQuiz.objects.filter(eleve=self.request.user).select_related('quiz')

    def perform_create(self, serializer):
        serializer.save(eleve=self.request.user)
