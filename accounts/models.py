from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('enseignant', 'Enseignant'),
        ('eleve', 'Élève'),
        ('parent', 'Parent'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='eleve')
    telephone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_enseignant(self):
        return self.role == 'enseignant'

    @property
    def is_eleve(self):
        return self.role == 'eleve'


class Etablissement(models.Model):
    TYPE_CHOICES = [
        ('primaire', 'École Primaire'),
        ('secondaire', 'Lycée / Collège'),
        ('franco_arabe', 'École Franco-Arabe'),
        ('daara', 'Daara Moderne'),
    ]
    nom = models.CharField(max_length=200)
    type_etablissement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    region = models.CharField(max_length=100)
    departement = models.CharField(max_length=100, blank=True)
    commune = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    directeur = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='etablissements_diriges'
    )
    date_creation = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Établissement'
        verbose_name_plural = 'Établissements'
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.get_type_etablissement_display()})"


class Classe(models.Model):
    NIVEAU_CHOICES = [
        # Primaire
        ('CI', 'Cours d\'Initiation (CI)'),
        ('CP', 'Cours Préparatoire (CP)'),
        ('CE1', 'Cours Élémentaire 1 (CE1)'),
        ('CE2', 'Cours Élémentaire 2 (CE2)'),
        ('CM1', 'Cours Moyen 1 (CM1)'),
        ('CM2', 'Cours Moyen 2 (CM2)'),
        # Secondaire
        ('6eme', 'Sixième (6ème)'),
        ('5eme', 'Cinquième (5ème)'),
        ('4eme', 'Quatrième (4ème)'),
        ('3eme', 'Troisième (3ème)'),
        ('2nde', 'Seconde (2nde)'),
        ('1ere', 'Première (1ère)'),
        ('terminale', 'Terminale'),
    ]
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE, related_name='classes')
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES)
    nom = models.CharField(max_length=50, help_text="Ex: CE2-A, 6ème-B")
    enseignant_principal = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={'role': 'enseignant'}, related_name='classes_principales'
    )
    annee_scolaire = models.CharField(max_length=9, help_text="Ex: 2024-2025")
    eleves = models.ManyToManyField(
        User, limit_choices_to={'role': 'eleve'}, related_name='classes', blank=True
    )

    class Meta:
        verbose_name = 'Classe'
        verbose_name_plural = 'Classes'
        ordering = ['etablissement', 'niveau', 'nom']

    def __str__(self):
        return f"{self.nom} - {self.etablissement.nom} ({self.annee_scolaire})"

    def get_niveau_cycle(self):
        primaires = ['CI', 'CP', 'CE1', 'CE2', 'CM1', 'CM2']
        return 'primaire' if self.niveau in primaires else 'secondaire'
