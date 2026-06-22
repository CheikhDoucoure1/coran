from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from quran.models import Surah, Verset


class Quiz(models.Model):
    TYPE_CHOICES = [
        ('memorisation', 'Test de Mémorisation'),
        ('comprehension', 'Test de Compréhension'),
        ('tajweed', 'Règles de Tajweed'),
        ('general', 'Évaluation Générale'),
    ]
    titre = models.CharField(max_length=200)
    type_quiz = models.CharField(max_length=20, choices=TYPE_CHOICES)
    niveau = models.ForeignKey('curriculum.NiveauScolaire', on_delete=models.CASCADE, related_name='quiz')
    surah = models.ForeignKey(Surah, on_delete=models.SET_NULL, null=True, blank=True, related_name='quiz')
    description = models.TextField(blank=True)
    duree_minutes = models.PositiveSmallIntegerField(default=30)
    note_maximale = models.DecimalField(max_digits=5, decimal_places=2, default=20.0)
    actif = models.BooleanField(default=True)
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    createur = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True,
        limit_choices_to={'role': 'enseignant'}, related_name='quiz_crees'
    )
    classes = models.ManyToManyField('accounts.Classe', blank=True, related_name='quiz')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quiz'
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} ({self.get_type_quiz_display()})"

    def get_nombre_questions(self):
        return self.questions.count()


class Question(models.Model):
    TYPE_CHOICES = [
        ('qcm', 'Choix Multiple (QCM)'),
        ('vf', 'Vrai ou Faux'),
        ('texte_lacunaire', 'Texte à Trous'),
        ('reponse_libre', 'Réponse Libre'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    type_question = models.CharField(max_length=20, choices=TYPE_CHOICES)
    enonce = models.TextField()
    enonce_arabe = models.TextField(blank=True)
    verset_reference = models.ForeignKey(
        Verset, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions_quiz'
    )
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    explication = models.TextField(blank=True, help_text="Explication de la bonne réponse")
    ordre = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['quiz', 'ordre']

    def __str__(self):
        return f"Q{self.ordre}: {self.enonce[:60]}..."

    def get_bonne_reponse(self):
        return self.reponses.filter(est_correcte=True).first()


class ReponseQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reponses')
    texte = models.TextField()
    texte_arabe = models.TextField(blank=True)
    est_correcte = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Réponse'
        verbose_name_plural = 'Réponses'

    def __str__(self):
        return f"{'✓' if self.est_correcte else '✗'} {self.texte[:50]}"


class TentativeQuiz(models.Model):
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('soumis', 'Soumis'),
        ('evalue', 'Évalué'),
    ]
    eleve = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        limit_choices_to={'role': 'eleve'}, related_name='tentatives'
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='tentatives')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='en_cours')
    note_obtenue = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    date_debut = models.DateTimeField(auto_now_add=True)
    date_soumission = models.DateTimeField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Tentative de Quiz'
        verbose_name_plural = 'Tentatives de Quiz'
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.eleve} - {self.quiz} ({self.statut})"

    @property
    def pourcentage_reussite(self):
        if self.note_obtenue is None:
            return None
        return int((self.note_obtenue / self.quiz.note_maximale) * 100)


class ReponseEleve(models.Model):
    tentative = models.ForeignKey(TentativeQuiz, on_delete=models.CASCADE, related_name='reponses_eleve')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reponse_choisie = models.ForeignKey(
        ReponseQuestion, on_delete=models.SET_NULL, null=True, blank=True
    )
    reponse_texte = models.TextField(blank=True)
    est_correcte = models.BooleanField(null=True, blank=True)
    points_obtenus = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Réponse Élève'
        verbose_name_plural = 'Réponses Élèves'
        unique_together = ['tentative', 'question']
