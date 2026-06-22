from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ProgressionMemorisation, SessionRecitation, BulletinCoranSenegal
from quran.models import Surah
from accounts.models import User, Classe


@login_required
def ma_progression(request):
    if request.user.role != 'eleve':
        return redirect('tableau_de_bord')

    progressions = ProgressionMemorisation.objects.filter(
        eleve=request.user
    ).select_related('surah').order_by('surah__numero')

    total_versets = sum(p.surah.nombre_versets for p in progressions)
    versets_memorises = sum(p.versets_memorises for p in progressions)
    pourcentage_global = int((versets_memorises / total_versets * 100) if total_versets else 0)

    return render(request, 'progress/ma_progression.html', {
        'progressions': progressions,
        'pourcentage_global': pourcentage_global,
        'versets_memorises': versets_memorises,
        'total_versets': total_versets,
    })


@login_required
def progression_eleve(request, eleve_id):
    if request.user.role not in ['enseignant', 'admin']:
        return redirect('tableau_de_bord')

    eleve = get_object_or_404(User, pk=eleve_id, role='eleve')
    progressions = ProgressionMemorisation.objects.filter(
        eleve=eleve
    ).select_related('surah').order_by('surah__numero')
    sessions = SessionRecitation.objects.filter(
        eleve=eleve
    ).select_related('surah', 'evaluateur').order_by('-date_session')[:20]

    return render(request, 'progress/progression_eleve.html', {
        'eleve': eleve,
        'progressions': progressions,
        'sessions': sessions,
    })


@login_required
def enregistrer_session(request):
    if request.user.role != 'enseignant':
        messages.error(request, "Seuls les enseignants peuvent enregistrer des récitations.")
        return redirect('tableau_de_bord')

    if request.method == 'POST':
        eleve_id = request.POST['eleve']
        surah_id = request.POST['surah']
        note = request.POST['note']

        session = SessionRecitation.objects.create(
            eleve_id=eleve_id,
            surah_id=surah_id,
            evaluateur=request.user,
            note=note,
            evaluation_qualitative=request.POST.get('evaluation_qualitative', 'satisfaisant'),
            tajweed_respecte=request.POST.get('tajweed_respecte') == 'on',
            makhraj_correct=request.POST.get('makhraj_correct') == 'on',
            rythme_adequat=request.POST.get('rythme_adequat') == 'on',
            observations=request.POST.get('observations', ''),
        )

        # Mise à jour de la progression
        progression, _ = ProgressionMemorisation.objects.get_or_create(
            eleve_id=eleve_id, surah_id=surah_id
        )
        progression.note_recitation = note
        progression.derniere_evaluation = timezone.now()
        versets_count = int(request.POST.get('versets_memorises', progression.versets_memorises))
        progression.versets_memorises = versets_count
        surah = get_object_or_404(Surah, pk=surah_id)
        if versets_count >= surah.nombre_versets:
            progression.statut = 'memorise'
        elif versets_count > 0:
            progression.statut = 'en_cours'
        progression.save()

        messages.success(request, "Session de récitation enregistrée.")
        return redirect('progression_eleve', eleve_id=eleve_id)

    classes = request.user.classes_principales.prefetch_related('eleves').all()
    sourates = Surah.objects.all()
    return render(request, 'progress/enregistrer_session.html', {
        'classes': classes,
        'sourates': sourates,
    })


@login_required
def mes_bulletins(request):
    if request.user.role == 'eleve':
        bulletins = BulletinCoranSenegal.objects.filter(
            eleve=request.user
        ).select_related('classe').order_by('-annee_scolaire', '-periode')
    else:
        return redirect('tableau_de_bord')
    return render(request, 'progress/bulletins.html', {'bulletins': bulletins})


@login_required
def tableau_classe(request, classe_id):
    if request.user.role not in ['enseignant', 'admin']:
        return redirect('tableau_de_bord')

    classe = get_object_or_404(Classe, pk=classe_id)
    eleves = classe.eleves.all()

    donnees_eleves = []
    for eleve in eleves:
        progressions = ProgressionMemorisation.objects.filter(eleve=eleve)
        memorisees = progressions.filter(statut__in=['memorise', 'maitrise']).count()
        en_cours = progressions.filter(statut='en_cours').count()
        donnees_eleves.append({
            'eleve': eleve,
            'memorisees': memorisees,
            'en_cours': en_cours,
            'total': progressions.count(),
        })

    return render(request, 'progress/tableau_classe.html', {
        'classe': classe,
        'donnees_eleves': donnees_eleves,
    })
