"""
Commande pour initialiser les données de démonstration.
Usage: python manage.py initialiser_donnees
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Etablissement, Classe

User = get_user_model()


class Command(BaseCommand):
    help = 'Initialise les données de démonstration pour Coran Sénégal'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Initialisation des données de démonstration...'))

        # Superuser admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                password='admin123',
                email='admin@quransenegal.sn',
                first_name='Administrateur',
                last_name='Système',
                role='admin',
            )
            self.stdout.write(self.style.SUCCESS('✓ Admin créé (admin / admin123)'))

        # Enseignant de démonstration
        if not User.objects.filter(username='enseignant1').exists():
            User.objects.create_user(
                username='enseignant1',
                password='demo1234',
                first_name='Moussa',
                last_name='Diallo',
                email='m.diallo@quransenegal.sn',
                role='enseignant',
                telephone='771234567',
            )
            self.stdout.write(self.style.SUCCESS('✓ Enseignant créé (enseignant1 / demo1234)'))

        # Élève de démonstration
        if not User.objects.filter(username='eleve1').exists():
            User.objects.create_user(
                username='eleve1',
                password='demo1234',
                first_name='Fatou',
                last_name='Ndiaye',
                email='f.ndiaye@eleve.sn',
                role='eleve',
            )
            self.stdout.write(self.style.SUCCESS('✓ Élève créé (eleve1 / demo1234)'))

        # Établissement
        etab, created = Etablissement.objects.get_or_create(
            nom='École Franco-Arabe Cheikh Anta Diop',
            defaults={
                'type_etablissement': 'franco_arabe',
                'region': 'Dakar',
                'departement': 'Dakar',
                'commune': 'Plateau',
                'telephone': '338210000',
                'email': 'contact@ecole-cad.sn',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Établissement créé'))

        # Classe CE2
        enseignant = User.objects.filter(username='enseignant1').first()
        eleve = User.objects.filter(username='eleve1').first()
        classe, created = Classe.objects.get_or_create(
            nom='CE2-A',
            defaults={
                'etablissement': etab,
                'niveau': 'CE2',
                'enseignant_principal': enseignant,
                'annee_scolaire': '2024-2025',
            }
        )
        if created and eleve:
            classe.eleves.add(eleve)
            self.stdout.write(self.style.SUCCESS('✓ Classe CE2-A créée avec l\'élève'))

        self.stdout.write(self.style.SUCCESS('\n✅ Données de démonstration initialisées avec succès !'))
        self.stdout.write('\nComptes disponibles:')
        self.stdout.write('  Admin       : admin / admin123')
        self.stdout.write('  Enseignant  : enseignant1 / demo1234')
        self.stdout.write('  Élève       : eleve1 / demo1234')
        self.stdout.write('\nAccédez à: http://127.0.0.1:8000/')
