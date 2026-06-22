from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import NiveauScolaire, ProgrammeCoranSenegal, PlanDeLecon, Ressource


def liste_niveaux(request):
    niveaux = NiveauScolaire.objects.prefetch_related('programme').all()
    return render(request, 'curriculum/niveaux.html', {'niveaux': niveaux})


def programme_niveau(request, niveau_code):
    niveau = get_object_or_404(NiveauScolaire, code=niveau_code)
    try:
        programme = niveau.programme
        sourates_s1 = programme.sourateniveau_set.filter(periode='S1').select_related('surah')
        sourates_s2 = programme.sourateniveau_set.filter(periode='S2').select_related('surah')
        sourates_annee = programme.sourateniveau_set.filter(periode='annee').select_related('surah')
    except ProgrammeCoranSenegal.DoesNotExist:
        programme = None
        sourates_s1 = sourates_s2 = sourates_annee = []

    plans = PlanDeLecon.objects.filter(niveau=niveau, statut='valide').select_related('surah')

    return render(request, 'curriculum/programme.html', {
        'niveau': niveau,
        'programme': programme,
        'sourates_s1': sourates_s1,
        'sourates_s2': sourates_s2,
        'sourates_annee': sourates_annee,
        'plans': plans,
    })


@login_required
def liste_plans_lecon(request):
    if request.user.role == 'enseignant':
        plans = PlanDeLecon.objects.filter(auteur=request.user).select_related('niveau', 'surah')
    else:
        plans = PlanDeLecon.objects.filter(statut='valide').select_related('niveau', 'surah')

    niveau_filtre = request.GET.get('niveau')
    if niveau_filtre:
        plans = plans.filter(niveau__code=niveau_filtre)

    niveaux = NiveauScolaire.objects.all()
    return render(request, 'curriculum/plans_lecon.html', {
        'plans': plans,
        'niveaux': niveaux,
        'niveau_filtre': niveau_filtre,
    })


@login_required
def detail_plan_lecon(request, pk):
    plan = get_object_or_404(PlanDeLecon, pk=pk)
    return render(request, 'curriculum/detail_plan.html', {'plan': plan})


@login_required
def creer_plan_lecon(request):
    if request.user.role not in ['enseignant', 'admin']:
        messages.error(request, "Vous n'avez pas la permission de créer un plan de leçon.")
        return redirect('liste_plans_lecon')

    if request.method == 'POST':
        from quran.models import Surah
        plan = PlanDeLecon(
            titre=request.POST['titre'],
            niveau_id=request.POST['niveau'],
            surah_id=request.POST['surah'],
            duree_minutes=request.POST.get('duree_minutes', 60),
            objectifs=request.POST['objectifs'],
            prerequis=request.POST.get('prerequis', ''),
            deroulement=request.POST['deroulement'],
            activites_eleves=request.POST.get('activites_eleves', ''),
            evaluation=request.POST.get('evaluation', ''),
            materiel_requis=request.POST.get('materiel_requis', ''),
            auteur=request.user,
            statut='brouillon',
        )
        plan.save()
        messages.success(request, "Plan de leçon créé avec succès !")
        return redirect('detail_plan_lecon', pk=plan.pk)

    niveaux = NiveauScolaire.objects.all()
    from quran.models import Surah
    sourates = Surah.objects.all()
    return render(request, 'curriculum/creer_plan.html', {
        'niveaux': niveaux,
        'sourates': sourates,
    })


def ressources(request):
    ressources_list = Ressource.objects.select_related('surah').all()
    type_filtre = request.GET.get('type')
    if type_filtre:
        ressources_list = ressources_list.filter(type_ressource=type_filtre)
    return render(request, 'curriculum/ressources.html', {
        'ressources': ressources_list,
        'type_filtre': type_filtre,
    })
