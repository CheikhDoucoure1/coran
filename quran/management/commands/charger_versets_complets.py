"""
Commande pour charger TOUS les versets des 114 sourates depuis l'API AlQuran.cloud.
Usage: python manage.py charger_versets_complets
       python manage.py charger_versets_complets --sourate 1        # une seule sourate
       python manage.py charger_versets_complets --debut 1 --fin 10 # plage de sourates
"""
import ssl
import time
import urllib.request
import urllib.error
import json

_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

from django.core.management.base import BaseCommand
from quran.models import Surah, Verset

API_BASE = "https://api.alquran.cloud/v1"


def fetch_json(url, retries=3):
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=15, context=_SSL_CTX) as resp:
                return json.loads(resp.read())
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise e


class Command(BaseCommand):
    help = 'Charge tous les versets des 114 sourates depuis api.alquran.cloud'

    def add_arguments(self, parser):
        parser.add_argument('--sourate', type=int, help='Numéro d\'une seule sourate à charger')
        parser.add_argument('--debut', type=int, default=1, help='Sourate de départ (défaut: 1)')
        parser.add_argument('--fin', type=int, default=114, help='Sourate de fin (défaut: 114)')
        parser.add_argument('--forcer', action='store_true', help='Réécrire les versets existants')

    def handle(self, *args, **options):
        if options['sourate']:
            numeros = [options['sourate']]
        else:
            numeros = list(range(options['debut'], options['fin'] + 1))

        total_crees = 0
        total_maj = 0
        erreurs = []

        self.stdout.write(self.style.MIGRATE_HEADING(
            f'\nChargement des versets pour {len(numeros)} sourate(s)...\n'
        ))

        for i, numero in enumerate(numeros, 1):
            try:
                surah = Surah.objects.get(numero=numero)
            except Surah.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Sourate {numero} non trouvée en DB, ignorée.'))
                continue

            deja_complet = surah.versets.count() == surah.nombre_versets
            if deja_complet and not options['forcer']:
                self.stdout.write(f'  S{numero:3d} {surah.nom_translittere:<25} déjà complet ({surah.nombre_versets} versets)')
                continue

            try:
                # Fetch Arabic text
                data_ar = fetch_json(f"{API_BASE}/surah/{numero}")
                ayahs_ar = data_ar['data']['ayahs']

                # Fetch French translation
                data_fr = fetch_json(f"{API_BASE}/surah/{numero}/fr.hamidullah")
                ayahs_fr = {a['numberInSurah']: a['text'] for a in data_fr['data']['ayahs']}

                crees = 0
                maj = 0
                for ayah in ayahs_ar:
                    num_verset = ayah['numberInSurah']
                    texte_arabe = ayah['text']
                    traduction_fr = ayahs_fr.get(num_verset, '')

                    defaults = {
                        'texte_arabe': texte_arabe,
                        'traduction_fr': traduction_fr,
                    }

                    if options['forcer']:
                        obj, created = Verset.objects.update_or_create(
                            surah=surah, numero=num_verset,
                            defaults=defaults
                        )
                        if created:
                            crees += 1
                        else:
                            maj += 1
                    else:
                        _, created = Verset.objects.get_or_create(
                            surah=surah, numero=num_verset,
                            defaults=defaults
                        )
                        if created:
                            crees += 1

                total_crees += crees
                total_maj += maj
                status = f'+{crees}' if crees else (f'~{maj} màj' if maj else 'ok')
                self.stdout.write(
                    self.style.SUCCESS(f'  S{numero:3d} {surah.nom_translittere:<25} {surah.nombre_versets:3d} versets [{status}]')
                )

                # Politesse envers l'API : pause toutes les 10 sourates
                if i % 10 == 0:
                    time.sleep(1)

            except Exception as e:
                erreurs.append((numero, surah.nom_translittere, str(e)))
                self.stdout.write(self.style.ERROR(f'  S{numero:3d} {surah.nom_translittere:<25} ERREUR: {e}'))

        self.stdout.write(self.style.MIGRATE_HEADING(
            f'\n✅ Terminé — {total_crees} versets créés, {total_maj} mis à jour.'
        ))
        if erreurs:
            self.stdout.write(self.style.WARNING(f'⚠️  {len(erreurs)} erreur(s) :'))
            for num, nom, err in erreurs:
                self.stdout.write(f'   S{num} {nom}: {err}')
