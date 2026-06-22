from django.db import models
from quran.models import Surah, Verset, Tajweed


class NiveauScolaire(models.Model):
    CYCLE_CHOICES = [
        ('primaire', 'Enseignement Primaire'),
        ('moyen', 'Enseignement Moyen (Collège)'),
        ('secondaire', 'Enseignement Secondaire (Lycée)'),
    ]
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES)
    ordre = models.PositiveSmallIntegerField(help_text="Ordre dans la progression scolaire")
    description = models.TextField(blank=True)
    competences_cibles = models.TextField(
        blank=True, help_text="Compétences visées pour ce niveau"
    )

    class Meta:
        verbose_name = 'Niveau Scolaire'
        verbose_name_plural = 'Niveaux Scolaires'
        ordering = ['ordre']

    def __str__(self):
        return f"{self.nom} ({self.get_cycle_display()})"


class ProgrammeCoranSenegal(models.Model):
    """Programme officiel d'éducation coranique du Sénégal par niveau."""
    niveau = models.OneToOneField(NiveauScolaire, on_delete=models.CASCADE, related_name='programme')
    objectifs_generaux = models.TextField()
    sourates_a_memoriser = models.ManyToManyField(
        Surah, through='SourateParNiveau', related_name='programmes'
    )
    heures_hebdomadaires = models.DecimalField(max_digits=4, decimal_places=1, default=2.0)
    regles_tajweed = models.ManyToManyField(Tajweed, blank=True, related_name='programmes')
    annee_scolaire = models.CharField(max_length=9, default='2024-2025')

    class Meta:
        verbose_name = 'Programme Coranique'
        verbose_name_plural = 'Programmes Coraniques'

    def __str__(self):
        return f"Programme {self.niveau} - {self.annee_scolaire}"


class SourateParNiveau(models.Model):
    PERIODE_CHOICES = [
        ('S1', 'Semestre 1'),
        ('S2', 'Semestre 2'),
        ('annee', 'Toute l\'année'),
    ]
    programme = models.ForeignKey(ProgrammeCoranSenegal, on_delete=models.CASCADE)
    surah = models.ForeignKey(Surah, on_delete=models.CASCADE)
    periode = models.CharField(max_length=10, choices=PERIODE_CHOICES, default='annee')
    versets_debut = models.PositiveSmallIntegerField(default=1)
    versets_fin = models.PositiveSmallIntegerField(null=True, blank=True)
    obligatoire = models.BooleanField(default=True)
    ordre_enseignement = models.PositiveSmallIntegerField(default=1)
    notes_enseignant = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Sourate par Niveau'
        verbose_name_plural = 'Sourates par Niveau'
        ordering = ['ordre_enseignement']

    def __str__(self):
        return f"{self.surah} → {self.programme.niveau}"


class PlanDeLecon(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('valide', 'Validé'),
        ('archive', 'Archivé'),
    ]
    titre = models.CharField(max_length=200)
    niveau = models.ForeignKey(NiveauScolaire, on_delete=models.CASCADE, related_name='plans_lecon')
    surah = models.ForeignKey(Surah, on_delete=models.CASCADE, related_name='plans_lecon')
    versets = models.ManyToManyField(Verset, blank=True, related_name='plans_lecon')
    duree_minutes = models.PositiveSmallIntegerField(default=60)
    objectifs = models.TextField()
    prerequis = models.TextField(blank=True)
    deroulement = models.TextField(help_text="Déroulement détaillé de la séance")
    activites_eleves = models.TextField(blank=True)
    evaluation = models.TextField(blank=True)
    materiel_requis = models.TextField(blank=True)
    auteur = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True,
        limit_choices_to={'role': 'enseignant'}
    )
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='brouillon')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Plan de Leçon'
        verbose_name_plural = 'Plans de Leçons'
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} - {self.niveau}"


class Ressource(models.Model):
    TYPE_CHOICES = [
        ('audio', 'Fichier Audio'),
        ('video', 'Vidéo'),
        ('pdf', 'Document PDF'),
        ('image', 'Image'),
        ('lien', 'Lien externe'),
    ]
    titre = models.CharField(max_length=200)
    type_ressource = models.CharField(max_length=10, choices=TYPE_CHOICES)
    fichier = models.FileField(upload_to='ressources/', blank=True, null=True)
    url_externe = models.URLField(blank=True)
    description = models.TextField(blank=True)
    niveau = models.ManyToManyField(NiveauScolaire, blank=True, related_name='ressources')
    surah = models.ForeignKey(Surah, on_delete=models.SET_NULL, null=True, blank=True, related_name='ressources')
    plan_lecon = models.ForeignKey(
        PlanDeLecon, on_delete=models.SET_NULL, null=True, blank=True, related_name='ressources'
    )
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ressource Pédagogique'
        verbose_name_plural = 'Ressources Pédagogiques'

    def __str__(self):
        return self.titre
