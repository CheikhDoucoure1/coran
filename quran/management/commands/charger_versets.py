"""
Commande pour charger les versets d'Al-Fatiha et sourates courtes.
Usage: python manage.py charger_versets
"""
from django.core.management.base import BaseCommand
from quran.models import Surah, Verset

VERSETS_AL_FATIHA = [
    (1, "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "Al-ḥamdu li-llāhi rabbi l-ʿālamīn",
     "Louange à Allah, Seigneur de l'univers,", "Bu baax bëgg Yàlla, boroom yëkëti àddina yi,"),
    (2, "الرَّحْمَٰنِ الرَّحِيمِ", "Ar-raḥmāni r-raḥīm",
     "le Tout Miséricordieux, le Très Miséricordieux,", "Jiitu Yàlla, Bëgg Yàlla,"),
    (3, "مَالِكِ يَوْمِ الدِّينِ", "Māliki yawmi d-dīn",
     "Maître du Jour de la rétribution.", "Boroom fan di jàngël dëkk,"),
    (4, "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ", "ʾIyyāka naʿbudu wa-ʾiyyāka nastaʿīn",
     "C'est Toi [Seul] que nous adorons, et c'est Toi [Seul] dont nous implorons le secours.", "Yow rekk la nu jëfandikoo, yow rekk la nu dëppoo,"),
    (5, "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ", "Ihdinā ṣ-ṣirāṭa l-mustaqīm",
     "Guide-nous dans le droit chemin,", "Wëcci ñu ci yoon bu dëggëer bi,"),
    (6, "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
     "Ṣirāṭa llaḏīna ʾanʿamta ʿalayhim ġayri l-maġḍūbi ʿalayhim wa-lā ḍ-ḍāllīn",
     "le chemin de ceux que Tu as comblés de faveurs, non pas de ceux qui ont encouru Ta colère, ni des égarés.",
     "Yoon yi ñu ko jëfandikoo di di ñenante ci, du yoon yi ñu ko daw, du yoon yi ñu weexe."),
]

VERSETS_IKHLAS = [
    (1, "قُلْ هُوَ اللَّهُ أَحَدٌ", "Qul huwa llāhu ʾaḥad",
     "Dis : « Il est Allah, [l'Unique,]", "Wax : Yàlla moo sax,"),
    (2, "اللَّهُ الصَّمَدُ", "Allāhu ṣ-ṣamad",
     "Allah, le Seul à être imploré pour ce que nous désirons.", "Yàlla moo sax, ñoom la ñu dëppoo,"),
    (3, "لَمْ يَلِدْ وَلَمْ يُولَدْ", "Lam yalid wa-lam yūlad",
     "Il n'a pas engendré, et n'a pas été engendré,", "Feeñalul, di weeñuló,"),
    (4, "وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ", "Wa-lam yakun lahu kufuwan ʾaḥad",
     "et Il n'a pas d'égal. »", "Kenn du ko jekk."),
]

VERSETS_FALAQ = [
    (1, "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ", "Qul ʾaʿūḏu bi-rabbi l-falaq",
     "Dis : « Je cherche protection auprès du Seigneur de l'Aube naissante,", "Wax: Ma loolu ci Boroom fajr bi,"),
    (2, "مِن شَرِّ مَا خَلَقَ", "Min šarri mā ḫalaق",
     "contre le mal de ce qu'Il a créé,", "ci bàkkaar bi moo dem ak sunu xam-xam,"),
    (3, "وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ", "Wa-min šarri ġāsiqin ʾiḏā waqab",
     "contre le mal de l'obscurité quand elle s'étend,", "ci bàkkaar bi moo dem ak guddi bi,"),
    (4, "وَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ", "Wa-min šarri n-naffāṯāti fī l-ʿuqad",
     "contre le mal de celles qui soufflent sur les nœuds,", "ci bàkkaar bi di tëb ci lakket yi,"),
    (5, "وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ", "Wa-min šarri ḥāsidin ʾiḏā ḥasad",
     "et contre le mal de l'envieux quand il envie. »", "ci bàkkaar bi di hasad."),
]

VERSETS_NAS = [
    (1, "قُلْ أَعُوذُ بِرَبِّ النَّاسِ", "Qul ʾaʿūḏu bi-rabbi n-nās",
     "Dis : « Je cherche protection auprès du Seigneur des hommes,", "Wax : Ma loolu ci Boroom doomu Aadama,"),
    (2, "مَلِكِ النَّاسِ", "Maliki n-nās",
     "du Roi des hommes,", "Boroom rëkki doomu Aadama,"),
    (3, "إِلَٰهِ النَّاسِ", "ʾIlāhi n-nās",
     "du Dieu des hommes,", "Yàlla gi doomu Aadama,"),
    (4, "مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ", "Min šarri l-waswāsi l-ḫannās",
     "contre le mal du mauvais conseiller, le furtif,", "ci bàkkaar bi di waswasa,"),
    (5, "الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ", "Allaḏī yuwaswisu fī ṣudūri n-nās",
     "qui souffle le mal dans les poitrines des hommes,", "ñi di waswas ci xol doomu Aadama,"),
    (6, "مِنَ الْجِنَّةِ وَالنَّاسِ", "Mina l-jinnati wa-n-nās",
     "qu'ils soient djinns ou hommes. »", "jinn ak doomu Aadama."),
]


class Command(BaseCommand):
    help = 'Charge les versets des sourates de base (Al-Fatiha, Ikhlas, Falaq, Nas)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Chargement des versets...'))

        data = {
            1: ('Al-Fatiha', VERSETS_AL_FATIHA),
            112: ('Al-Ikhlas', VERSETS_IKHLAS),
            113: ('Al-Falaq', VERSETS_FALAQ),
            114: ('An-Nas', VERSETS_NAS),
        }

        for numero, (nom, versets) in data.items():
            try:
                surah = Surah.objects.get(numero=numero)
                count = 0
                for verset_data in versets:
                    num, arabe, translit, fr, wo = verset_data
                    _, created = Verset.objects.get_or_create(
                        surah=surah, numero=num,
                        defaults={
                            'texte_arabe': arabe,
                            'translitteration': translit,
                            'traduction_fr': fr,
                            'traduction_wolof': wo,
                        }
                    )
                    if created:
                        count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ {nom}: {count} versets chargés'))
            except Surah.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Sourate {numero} non trouvée. Chargez d\'abord les fixtures.'))

        self.stdout.write(self.style.SUCCESS('\n✅ Versets chargés avec succès !'))
