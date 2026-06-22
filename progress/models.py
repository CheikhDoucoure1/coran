from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from quran.models import Surah, Verset


class ProgressionMemorisation(models.Model):
    STATUT_CHOICES = [
        ('non_commence', 'Non commencé'),
        ('en_cours', 'En cours'),
        ('memorise', 'Mémorisé'),
        ('maitrise', 'Maîtrisé'),
    ]
    eleve = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        limit_choices_to={'role': 'eleve'}, related_name='progressions'
    )
    surah = models.ForeignKey(Surah, on_delete=models.CASCADE, related_name='progressions')
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='non_commence')
    versets_memorises = models.PositiveSmallIntegerField(default=0)
    note_recitation = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    commentaire_enseignant = models.TextField(blank=True)
    date_debut = models.DateField(null=True, blank=True)
    date_maitrise = models.DateField(null=True, blank=True)
    derniere_evaluation = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Progression Mémorisation'
        verbose_name_plural = 'Progressions Mémorisation'
        unique_together = ['eleve', 'surah']
        ordering = ['-derniere_evaluation']

    def __str__(self):
        return f"{self.eleve} - {self.surah} ({self.get_statut_display()})"

    @property
    def pourcentage(self):
        if self.surah.nombre_versets == 0:
            return 0
        return int((self.versets_memorises / self.surah.nombre_versets) * 100)


class SessionRecitation(models.Model):
    EVALUATION_CHOICES = [
        ('excellent', 'Excellent'),
        ('bien', 'Bien'),
        ('satisfaisant', 'Satisfaisant'),
        ('a_revoir', 'À revoir'),
    ]
    eleve = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        limit_choices_to={'role': 'eleve'}, related_name='sessions_recitation'
    )
    surah = models.ForeignKey(Surah, on_delete=models.CASCADE, related_name='sessions')
    versets_recites = models.ManyToManyField(Verset, blank=True)
    evaluateur = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True,
        limit_choices_to={'role': 'enseignant'}, related_name='evaluations_donnees'
    )
    note = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    evaluation_qualitative = models.CharField(max_length=20, choices=EVALUATION_CHOICES)
    tajweed_respecte = models.BooleanField(default=False)
    makhraj_correct = models.BooleanField(default=False)
    rythme_adequat = models.BooleanField(default=False)
    observations = models.TextField(blank=True)
    date_session = models.DateTimeField(auto_now_add=True)
    classe = models.ForeignKey(
        'accounts.Classe', on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = 'Session de Récitation'
        verbose_name_plural = 'Sessions de Récitation'
        ordering = ['-date_session']

    def __str__(self):
        return f"Récitation de {self.eleve} - {self.surah} ({self.date_session.date()})"


class BulletinCoranSenegal(models.Model):
    PERIODE_CHOICES = [
        ('S1', 'Semestre 1'),
        ('S2', 'Semestre 2'),
        ('annuel', 'Annuel'),
    ]
    eleve = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        limit_choices_to={'role': 'eleve'}, related_name='bulletins'
    )
    classe = models.ForeignKey('accounts.Classe', on_delete=models.CASCADE)
    periode = models.CharField(max_length=10, choices=PERIODE_CHOICES)
    annee_scolaire = models.CharField(max_length=9)
    note_memorisation = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    note_recitation = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    note_tajweed = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    note_comprehension = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        null=True, blank=True
    )
    appreciation = models.TextField(blank=True)
    sourates_validees = models.ManyToManyField(Surah, blank=True, related_name='bulletins')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Bulletin Coranique'
        verbose_name_plural = 'Bulletins Coraniques'
        unique_together = ['eleve', 'classe', 'periode', 'annee_scolaire']

    def __str__(self):
        return f"Bulletin {self.eleve} - {self.periode} {self.annee_scolaire}"

    @property
    def moyenne_generale(self):
        notes = [self.note_memorisation, self.note_recitation, self.note_tajweed]
        if self.note_comprehension:
            notes.append(self.note_comprehension)
        return sum(notes) / len(notes)
