from django.db import models


class Surah(models.Model):
    REVELATION_CHOICES = [
        ('mecquoise', 'Mecquoise'),
        ('medinoise', 'Médinoise'),
    ]
    numero = models.PositiveSmallIntegerField(unique=True)
    nom_arabe = models.CharField(max_length=100)
    nom_translittere = models.CharField(max_length=100)
    nom_francais = models.CharField(max_length=100)
    nombre_versets = models.PositiveSmallIntegerField()
    type_revelation = models.CharField(max_length=15, choices=REVELATION_CHOICES)
    ordre_revelation = models.PositiveSmallIntegerField()
    description_fr = models.TextField(blank=True, help_text="Description pédagogique en français")
    audio_url = models.URLField(blank=True)
    niveau_difficulte = models.PositiveSmallIntegerField(
        default=1, choices=[(i, str(i)) for i in range(1, 6)],
        help_text="1 = Facile (pour CI/CP), 5 = Difficile (pour Terminale)"
    )

    class Meta:
        verbose_name = 'Sourate'
        verbose_name_plural = 'Sourates'
        ordering = ['numero']

    def __str__(self):
        return f"{self.numero}. {self.nom_translittere} ({self.nom_francais})"


class Verset(models.Model):
    surah = models.ForeignKey(Surah, on_delete=models.CASCADE, related_name='versets')
    numero = models.PositiveSmallIntegerField()
    texte_arabe = models.TextField()
    translitteration = models.TextField(blank=True)
    traduction_fr = models.TextField(blank=True)
    traduction_wolof = models.TextField(blank=True)
    notes_pedagogiques = models.TextField(blank=True)
    audio_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Verset'
        verbose_name_plural = 'Versets'
        ordering = ['surah', 'numero']
        unique_together = ['surah', 'numero']

    def __str__(self):
        return f"S.{self.surah.numero}:V.{self.numero}"


class Tajweed(models.Model):
    CATEGORIE_CHOICES = [
        ('makhraj', 'Makhraj (Point d\'articulation)'),
        ('sifat', 'Sifat (Caractéristiques)'),
        ('madd', 'Madd (Prolongation)'),
        ('waqf', 'Waqf (Arrêt)'),
        ('idgham', 'Idgham (Assimilation)'),
        ('ikhfa', 'Ikhfa (Occultation)'),
        ('iqlab', 'Iqlab (Changement)'),
    ]
    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    description_fr = models.TextField()
    exemple_arabe = models.CharField(max_length=200, blank=True)
    niveau_scolaire = models.CharField(
        max_length=20, blank=True,
        help_text="Niveau scolaire recommandé pour introduire cette règle"
    )

    class Meta:
        verbose_name = 'Règle de Tajweed'
        verbose_name_plural = 'Règles de Tajweed'

    def __str__(self):
        return f"{self.nom} ({self.get_categorie_display()})"


class GlossaireIslamique(models.Model):
    terme_arabe = models.CharField(max_length=100)
    terme_francais = models.CharField(max_length=100)
    terme_wolof = models.CharField(max_length=100, blank=True)
    definition_fr = models.TextField()
    exemple_utilisation = models.TextField(blank=True)
    verset_reference = models.ForeignKey(
        Verset, on_delete=models.SET_NULL, null=True, blank=True, related_name='glossaire'
    )

    class Meta:
        verbose_name = 'Terme du Glossaire'
        verbose_name_plural = 'Glossaire Islamique'
        ordering = ['terme_francais']

    def __str__(self):
        return f"{self.terme_arabe} - {self.terme_francais}"
