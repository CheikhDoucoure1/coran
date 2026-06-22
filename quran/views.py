from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Surah, Verset, GlossaireIslamique, Tajweed


def liste_sourates(request):
    sourates = Surah.objects.all()
    q = request.GET.get('q', '')
    if q:
        sourates = sourates.filter(
            Q(nom_translittere__icontains=q) |
            Q(nom_francais__icontains=q) |
            Q(nom_arabe__icontains=q)
        )
    niveau = request.GET.get('niveau')
    if niveau:
        sourates = sourates.filter(niveau_difficulte=niveau)
    return render(request, 'quran/sourates.html', {
        'sourates': sourates,
        'query': q,
        'niveau_filtre': niveau,
    })


def detail_sourate(request, numero):
    surah = get_object_or_404(Surah, numero=numero)
    versets = surah.versets.all()
    prev_surah = Surah.objects.filter(numero=numero - 1).first()
    next_surah = Surah.objects.filter(numero=numero + 1).first()

    progression = None
    if request.user.is_authenticated and request.user.role == 'eleve':
        from progress.models import ProgressionMemorisation
        progression, _ = ProgressionMemorisation.objects.get_or_create(
            eleve=request.user, surah=surah
        )

    return render(request, 'quran/detail_sourate.html', {
        'surah': surah,
        'versets': versets,
        'prev_surah': prev_surah,
        'next_surah': next_surah,
        'progression': progression,
    })


def detail_verset(request, surah_numero, verset_numero):
    surah = get_object_or_404(Surah, numero=surah_numero)
    verset = get_object_or_404(Verset, surah=surah, numero=verset_numero)
    return render(request, 'quran/detail_verset.html', {
        'surah': surah,
        'verset': verset,
    })


def glossaire(request):
    termes = GlossaireIslamique.objects.select_related('verset_reference').all()
    q = request.GET.get('q', '')
    if q:
        termes = termes.filter(
            Q(terme_arabe__icontains=q) |
            Q(terme_francais__icontains=q) |
            Q(terme_wolof__icontains=q) |
            Q(definition_fr__icontains=q)
        )
    return render(request, 'quran/glossaire.html', {'termes': termes, 'query': q})


def tajweed_list(request):
    categorie_filtre = request.GET.get('categorie', '')
    q = request.GET.get('q', '')

    regles = Tajweed.objects.all().order_by('categorie', 'nom')
    if categorie_filtre:
        regles = regles.filter(categorie=categorie_filtre)
    if q:
        regles = regles.filter(
            Q(nom__icontains=q) |
            Q(description_fr__icontains=q) |
            Q(exemple_arabe__icontains=q)
        )

    CATEGORIES_META = {
        'makhraj': {'label': "Makhraj — Points d'articulation", 'couleur': 'success',   'icone': 'bi-soundwave'},
        'sifat':   {'label': 'Sifat — Caractéristiques',        'couleur': 'primary',   'icone': 'bi-stars'},
        'madd':    {'label': 'Madd — Prolongations',            'couleur': 'warning',   'icone': 'bi-arrows-expand'},
        'idgham':  {'label': 'Idghâm — Assimilation',           'couleur': 'info',      'icone': 'bi-link-45deg'},
        'ikhfa':   {'label': 'Ikhfâ — Occultation',             'couleur': 'secondary', 'icone': 'bi-eye-slash'},
        'iqlab':   {'label': 'Iqlab — Substitution',            'couleur': 'danger',    'icone': 'bi-arrow-left-right'},
        'waqf':    {'label': 'Waqf — Arrêts',                   'couleur': 'dark',      'icone': 'bi-pause-circle'},
    }
    toutes_categories = [
        {'key': k, **v, 'count': Tajweed.objects.filter(categorie=k).count()}
        for k, v in CATEGORIES_META.items()
    ]

    return render(request, 'quran/tajweed.html', {
        'regles': regles,
        'toutes_categories': toutes_categories,
        'categorie_filtre': categorie_filtre,
        'categories_meta': CATEGORIES_META,
        'query': q,
        'total': Tajweed.objects.count(),
    })
