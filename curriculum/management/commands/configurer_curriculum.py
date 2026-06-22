"""
Configure le programme coranique pour les 13 niveaux scolaires sénégalais.
Usage:
    python manage.py configurer_curriculum            # créer tout
    python manage.py configurer_curriculum --reset    # supprimer et recréer
"""
from django.core.management.base import BaseCommand
from curriculum.models import NiveauScolaire, ProgrammeCoranSenegal, SourateParNiveau
from quran.models import Surah, Tajweed


# ─── Données du curriculum ────────────────────────────────────────────────────
# Format: niveau_code → {
#   objectifs, heures,
#   sourates: [(surah_numero, periode, v_debut, v_fin, obligatoire, ordre, notes)],
#   tajweed_categories: [liste de catégories Tajweed à lier]
# }

CURRICULUM = {

    # ══════════════════════════════════════════════
    #  PRIMAIRE
    # ══════════════════════════════════════════════

    "CI": {
        "objectifs": (
            "Initier l'élève à la récitation du Coran. Mémoriser Al-Fatiha et les 5 sourates "
            "les plus courtes du Juz' Amma. Reconnaître les lettres arabes à l'oral."
        ),
        "heures": 2.0,
        "sourates": [
            # (numero, periode, v_debut, v_fin, obligatoire, ordre, notes)
            (1,   "annee", 1, 7,    True,  1, "Sourate fondamentale — récitée dans chaque prière"),
            (114, "S1",    1, 6,    True,  2, "An-Nas : première sourate de protection"),
            (113, "S1",    1, 5,    True,  3, "Al-Falaq : complémentaire à An-Nas"),
            (112, "S2",    1, 4,    True,  4, "Al-Ikhlas : pilier de la foi en l'Unicité d'Allah"),
            (110, "S2",    1, 3,    True,  5, "An-Nasr : victoire divine, sourate courte accessible"),
        ],
        "tajweed_categories": ["makhraj"],
    },

    "CP": {
        "objectifs": (
            "Consolider la mémorisation d'Al-Fatiha et des sourates du CI. Mémoriser 5 nouvelles "
            "sourates courtes. Initiation à la prononciation correcte des lettres (makhraj)."
        ),
        "heures": 2.0,
        "sourates": [
            (1,   "annee", 1, 7,    True,  1, "Révision et consolidation"),
            (111, "S1",    1, 5,    True,  2, "Al-Masad : sourate narrative simple"),
            (109, "S1",    1, 6,    True,  3, "Al-Kafirun : affirmation de la foi"),
            (108, "S1",    1, 3,    True,  4, "Al-Kawthar : sourate très courte"),
            (107, "S2",    1, 7,    True,  5, "Al-Ma'un : valeurs islamiques essentielles"),
            (106, "S2",    1, 4,    True,  6, "Quraysh : contexte historique simple"),
        ],
        "tajweed_categories": ["makhraj", "sifat"],
    },

    "CE1": {
        "objectifs": (
            "Mémoriser 6 nouvelles sourates du Juz' Amma. Lire l'arabe couramment. "
            "Comprendre le sens général des sourates mémorisées. Initiation à la Qalqala."
        ),
        "heures": 2.0,
        "sourates": [
            (1,   "annee", 1, 7,    True,  1, "Révision permanente"),
            (105, "S1",    1, 5,    True,  2, "Al-Fil : récit historique accessible"),
            (104, "S1",    1, 9,    True,  3, "Al-Humaza : valeurs morales"),
            (103, "S1",    1, 3,    True,  4, "Al-Asr : sourate aux 3 versets fondateurs"),
            (102, "S2",    1, 8,    True,  5, "At-Takathur : mise en garde contre les richesses"),
            (101, "S2",    1, 11,   True,  6, "Al-Qari'a : description du Jour Dernier"),
            (100, "S2",    1, 11,   True,  7, "Al-Adiyat : rythme sonore, poésie coranique"),
        ],
        "tajweed_categories": ["makhraj", "sifat"],
    },

    "CE2": {
        "objectifs": (
            "Mémoriser 7 nouvelles sourates. Appliquer les règles de base du Nûn sâkin "
            "(Izhâr, Iqlab). Comprendre le vocabulaire coranique des sourates étudiées."
        ),
        "heures": 2.0,
        "sourates": [
            (99,  "S1",    1, 8,    True,  1, "Az-Zalzala : description poignante du Jour Dernier"),
            (98,  "S1",    1, 8,    True,  2, "Al-Bayyina : la preuve de la vérité"),
            (97,  "S1",    1, 5,    True,  3, "Al-Qadr : nuit de la révélation du Coran"),
            (96,  "S2",    1, 5,    True,  4, "Al-Alaq v.1-5 : premiers versets révélés — 'Lis !'"),
            (95,  "S2",    1, 8,    True,  5, "At-Tin : le figuier — dignité de l'Homme"),
            (94,  "S2",    1, 8,    True,  6, "Ash-Sharh : l'élargissement du cœur"),
        ],
        "tajweed_categories": ["makhraj", "sifat", "ikhfa", "iqlab"],
    },

    "CM1": {
        "objectifs": (
            "Mémoriser 6 sourates supplémentaires du Juz' Amma. Maîtriser les règles du Nûn sâkin "
            "et Tanwîn (Idghâm, Ikhfâ, Iqlab, Izhâr). Comprendre le sens général des sourates. "
            "Récitation du Juz' Amma partiel avec Tajweed."
        ),
        "heures": 2.5,
        "sourates": [
            (93,  "S1",    1, 11,   True,  1, "Ad-Duha : réconfort et espérance"),
            (92,  "S1",    1, 21,   True,  2, "Al-Layl : la nuit — antithèses morales"),
            (91,  "S1",    1, 15,   True,  3, "Ash-Shams : le soleil — purification de l'âme"),
            (90,  "S2",    1, 20,   True,  4, "Al-Balad : la cité — le chemin escarpé"),
            (89,  "S2",    1, 30,   True,  5, "Al-Fajr : l'aurore — nations passées"),
            (88,  "S2",    1, 26,   True,  6, "Al-Ghashiya : l'enveloppant — scènes du Jugement"),
        ],
        "tajweed_categories": ["makhraj", "sifat", "idgham", "ikhfa", "iqlab"],
    },

    "CM2": {
        "objectifs": (
            "Compléter la mémorisation du Juz' Amma (sourates 78-87). Réciter l'intégralité "
            "du Juz' Amma avec les règles de Tajweed. Maîtriser les prolongations (Madd) de base."
        ),
        "heures": 2.5,
        "sourates": [
            (87,  "S1",    1, 19,   True,  1, "Al-A'la : le Très-Haut — Tajweed prononciation ع"),
            (86,  "S1",    1, 17,   True,  2, "At-Tariq : l'astre nocturne"),
            (85,  "S1",    1, 22,   True,  3, "Al-Buruj : les constellations — martyre des croyants"),
            (84,  "S2",    1, 25,   True,  4, "Al-Inshiqaq : la fente du ciel"),
            (83,  "S2",    1, 36,   True,  5, "Al-Mutaffifin : les fraudeurs"),
            (82,  "S2",    1, 19,   True,  6, "Al-Infitar : déchirure du ciel — Jugement Dernier"),
        ],
        "tajweed_categories": ["makhraj", "sifat", "madd", "idgham", "ikhfa", "iqlab", "waqf"],
    },

    # ══════════════════════════════════════════════
    #  MOYEN (COLLÈGE)
    # ══════════════════════════════════════════════

    "6eme": {
        "objectifs": (
            "Mémoriser les sourates du début du Juz' 29 (An-Naba à Al-Mursalat). "
            "Étudier les points d'articulation (Makhraj) de manière systématique. "
            "Introduction à l'exégèse simplifiée (Tafsir) des sourates mémorisées."
        ),
        "heures": 3.0,
        "sourates": [
            (81,  "S1",    1, 29,   True,  1, "At-Takwir : bouleversement cosmique"),
            (80,  "S1",    1, 42,   True,  2, "Abasa : épisode éducatif — humilité du Prophète ﷺ"),
            (79,  "S1",    1, 46,   True,  3, "An-Nazi'at : les arracheurs"),
            (78,  "S2",    1, 40,   True,  4, "An-Naba : la grande nouvelle"),
            (77,  "S2",    1, 50,   True,  5, "Al-Mursalat : les envoyés"),
            (76,  "S2",    1, 31,   False, 6, "Al-Insan : l'homme — sourate complémentaire"),
        ],
        "tajweed_categories": ["makhraj", "sifat", "madd", "waqf"],
    },

    "5eme": {
        "objectifs": (
            "Mémoriser les sourates Al-Qiyama à Al-Muzzammil (Juz 29 suite). "
            "Maîtriser les caractéristiques des lettres (Sifat). "
            "Étude du sens et du contexte de révélation (Asbab An-Nuzul) des sourates."
        ),
        "heures": 3.0,
        "sourates": [
            (75,  "S1",    1, 40,   True,  1, "Al-Qiyama : la résurrection"),
            (74,  "S1",    1, 56,   True,  2, "Al-Muddaththir : enveloppé — début de la prédication"),
            (73,  "S1",    1, 20,   True,  3, "Al-Muzzammil : l'enveloppé — prière de nuit"),
            (72,  "S2",    1, 28,   True,  4, "Al-Jinn : les djinns témoins du Coran"),
            (71,  "S2",    1, 28,   True,  5, "Nuh : le prophète Noé — la patience"),
            (70,  "S2",    1, 44,   False, 6, "Al-Ma'arij : les degrés d'élévation"),
        ],
        "tajweed_categories": ["makhraj", "sifat", "madd", "idgham", "waqf"],
    },

    "4eme": {
        "objectifs": (
            "Mémoriser Al-Haqqa, Al-Qalam et Al-Mulk. Étudier les règles de pause (Waqf). "
            "Introduction aux sciences coraniques (mushafs, qira'at, i'jaz). "
            "Comprendre les thèmes théologiques des sourates."
        ),
        "heures": 3.0,
        "sourates": [
            (69,  "S1",    1, 52,   True,  1, "Al-Haqqa : la réalité inévitable — Jugement"),
            (68,  "S1",    1, 52,   True,  2, "Al-Qalam : la plume — valeur du savoir"),
            (67,  "S1",    1, 30,   True,  3, "Al-Mulk : la royauté — sourate protectrice"),
            (66,  "S2",    1, 12,   True,  4, "At-Tahrim : vie familiale des croyants"),
            (65,  "S2",    1, 12,   True,  5, "At-Talaq : règles du divorce islamique"),
            (64,  "S2",    1, 18,   False, 6, "At-Taghabun : la dépossession"),
        ],
        "tajweed_categories": ["makhraj", "sifat", "madd", "waqf"],
    },

    "3eme": {
        "objectifs": (
            "Achever la mémorisation du Juz' 28 (Al-Mujadila à Al-Munafiqun). "
            "Révision complète du Tajweed. Maîtriser la lecture avec waqf et ibtida'. "
            "Préparation à l'examen de fin de collège avec exégèse de sourates choisies."
        ),
        "heures": 3.0,
        "sourates": [
            (63,  "S1",    1, 11,   True,  1, "Al-Munafiqun : caractéristiques de l'hypocrite"),
            (62,  "S1",    1, 11,   True,  2, "Al-Jumu'a : importance du vendredi"),
            (61,  "S1",    1, 14,   True,  3, "As-Saff : combattre dans les rangs d'Allah"),
            (60,  "S2",    1, 13,   True,  4, "Al-Mumtahana : relations avec les non-croyants"),
            (59,  "S2",    1, 24,   True,  5, "Al-Hashr : exil des Banu Nadir"),
            (58,  "S2",    1, 22,   False, 6, "Al-Mujadila : la discussion — droit des femmes"),
            (36,  "annee", 1, 83,   False, 7, "Ya-Sin : cœur du Coran — révision et Tafsir"),
        ],
        "tajweed_categories": ["makhraj", "sifat", "madd", "idgham", "ikhfa", "iqlab", "waqf"],
    },

    # ══════════════════════════════════════════════
    #  SECONDAIRE (LYCÉE)
    # ══════════════════════════════════════════════

    "2nde": {
        "objectifs": (
            "Mémoriser Ar-Rahman, Al-Waqi'a et Al-Hadid. Révision et approfondissement de Ya-Sin. "
            "Maîtrise complète du Tajweed. Introduction à l'exégèse des grandes sourates (Al-Kahf). "
            "Étude du vocabulaire coranique et de la grammaire arabe coranique."
        ),
        "heures": 3.0,
        "sourates": [
            (55,  "S1",    1, 78,   True,  1, "Ar-Rahman : la Miséricorde divine — bienfaits répétés"),
            (56,  "S1",    1, 96,   True,  2, "Al-Waqi'a : l'événement — trois catégories de gens"),
            (57,  "S2",    1, 29,   True,  3, "Al-Hadid : le fer — lumière et dépense pour Allah"),
            (18,  "S2",    1, 30,   True,  4, "Al-Kahf v.1-30 : la caverne — récit des jeunes croyants"),
            (36,  "annee", 1, 83,   False, 5, "Ya-Sin : révision et Tafsir approfondi"),
        ],
        "tajweed_categories": ["makhraj", "sifat", "madd", "idgham", "ikhfa", "iqlab", "waqf"],
    },

    "1ere": {
        "objectifs": (
            "Mémoriser Al-Baqara (versets choisis : 1-5, 255-257, 285-286) et Al-Kahf complet. "
            "Étude de l'exégèse thématique : foi, prière, aumône, pèlerinage. "
            "Lier les versets coraniques aux piliers de l'Islam."
        ),
        "heures": 3.0,
        "sourates": [
            (2,   "S1",    1,  5,   True,  1, "Al-Baqara v.1-5 : les croyants vertueux"),
            (2,   "S1",    255, 257, True,  2, "Ayat Al-Kursi (2:255-257) : verset du Trône"),
            (2,   "S1",    285, 286, True,  3, "Al-Baqara v.285-286 : l'Amen du Messager"),
            (18,  "S2",    1,  110, True,  4, "Al-Kahf intégral : les quatre récits"),
            (67,  "annee", 1,  30,  False, 5, "Al-Mulk : révision et maîtrise totale"),
        ],
        "tajweed_categories": ["makhraj", "sifat", "madd", "idgham", "ikhfa", "iqlab", "waqf"],
    },

    "terminale": {
        "objectifs": (
            "Maîtriser Al-Baqara (sections fondamentales) et Al-Imran (1-100). "
            "Rédiger un commentaire coranique structuré. Comprendre les règles d'abrogation "
            "(Nasikh et Mansukh). Préparer l'épreuve de CFEE/Baccalauréat islamique."
        ),
        "heures": 3.0,
        "sourates": [
            (2,   "S1",    1,   50,  True,  1, "Al-Baqara v.1-50 : foi, prière, récit des Israélites"),
            (2,   "S1",    153, 177, True,  2, "Al-Baqara v.153-177 : patience, jihad, Ka'ba, bienfaisance"),
            (3,   "S2",    1,   50,  True,  3, "Al-Imran v.1-50 : Unicité, naissance de Jésus, vérité"),
            (3,   "S2",    100, 200, True,  4, "Al-Imran v.100-200 : Uhud, persévérance, Paradis"),
            (36,  "annee", 1,   83,  False, 5, "Ya-Sin : maîtrise totale avec Tafsir"),
            (18,  "annee", 1,   110, False, 6, "Al-Kahf : révision et commentaire écrit"),
        ],
        "tajweed_categories": ["makhraj", "sifat", "madd", "idgham", "ikhfa", "iqlab", "waqf"],
    },
}


class Command(BaseCommand):
    help = 'Configure le programme coranique pour les 13 niveaux scolaires'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', action='store_true',
            help='Supprimer les programmes existants avant de recréer'
        )

    def handle(self, *args, **options):
        if options['reset']:
            deleted = ProgrammeCoranSenegal.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'  {deleted[0]} programme(s) supprimé(s).'))

        self.stdout.write(self.style.MIGRATE_HEADING('\nConfiguration du curriculum coranique...\n'))

        total_prog = 0
        total_spn = 0
        erreurs = []

        for code, data in CURRICULUM.items():
            try:
                niveau = NiveauScolaire.objects.get(code=code)
            except NiveauScolaire.DoesNotExist:
                erreurs.append(f'Niveau {code} introuvable')
                continue

            prog, created = ProgrammeCoranSenegal.objects.get_or_create(
                niveau=niveau,
                defaults={
                    'objectifs_generaux': data['objectifs'],
                    'heures_hebdomadaires': data['heures'],
                }
            )
            if not created:
                prog.objectifs_generaux = data['objectifs']
                prog.heures_hebdomadaires = data['heures']
                prog.save()

            # Lier les règles de Tajweed pertinentes
            tajweed_ids = Tajweed.objects.filter(
                categorie__in=data['tajweed_categories']
            ).values_list('id', flat=True)
            prog.regles_tajweed.set(tajweed_ids)

            # Créer les SourateParNiveau
            spn_crees = 0
            for (num, periode, v_debut, v_fin, obligatoire, ordre, notes) in data['sourates']:
                try:
                    surah = Surah.objects.get(numero=num)
                except Surah.DoesNotExist:
                    erreurs.append(f'Sourate {num} introuvable pour {code}')
                    continue

                # Chercher un SPN existant pour cette combinaison programme+surah+ordre
                spn, spn_created = SourateParNiveau.objects.get_or_create(
                    programme=prog,
                    surah=surah,
                    ordre_enseignement=ordre,
                    defaults={
                        'periode': periode,
                        'versets_debut': v_debut,
                        'versets_fin': v_fin,
                        'obligatoire': obligatoire,
                        'notes_enseignant': notes,
                    }
                )
                if not spn_created:
                    spn.periode = periode
                    spn.versets_debut = v_debut
                    spn.versets_fin = v_fin
                    spn.obligatoire = obligatoire
                    spn.notes_enseignant = notes
                    spn.save()
                    spn_crees += 1
                else:
                    spn_crees += 1
                total_spn += 1

            nb_tajweed = prog.regles_tajweed.count()
            self.stdout.write(
                self.style.SUCCESS(
                    f'  {"✓":2s} {code:<10} {niveau.nom:<35} '
                    f'{len(data["sourates"]):2d} sourates | '
                    f'{nb_tajweed:2d} règles Tajweed'
                )
            )
            total_prog += 1

        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING(
            f'✅  {total_prog} programmes créés/mis à jour — '
            f'{total_spn} entrées sourates configurées.'
        ))
        if erreurs:
            self.stdout.write(self.style.WARNING(f'\n⚠️  {len(erreurs)} erreur(s) :'))
            for e in erreurs:
                self.stdout.write(f'   {e}')
