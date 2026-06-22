from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg
from .models import User, Etablissement, Classe
from .forms import InscriptionEtablissementForm
from progress.models import ProgressionMemorisation, BulletinCoranSenegal
from quiz.models import TentativeQuiz


def accueil(request):
    if request.user.is_authenticated:
        return redirect('tableau_de_bord')
    return render(request, 'accueil.html')


def inscription_etablissement(request):
    if request.user.is_authenticated:
        return redirect('tableau_de_bord')
    form = InscriptionEtablissementForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user, etablissement = form.save()
        login(request, user)
        messages.success(
            request,
            f"Bienvenue ! Le compte de « {etablissement.nom} » a été créé avec succès."
        )
        return redirect('tableau_de_bord')
    return render(request, 'accounts/inscription_etablissement.html', {'form': form})


def connexion(request):
    if request.user.is_authenticated:
        return redirect('tableau_de_bord')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Bienvenue {user.get_full_name() or user.username} !")
            return redirect(request.GET.get('next', 'tableau_de_bord'))
        messages.error(request, "Identifiants incorrects. Veuillez réessayer.")
    return render(request, 'accounts/connexion.html')


def deconnexion(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('accueil')


@login_required
def tableau_de_bord(request):
    user = request.user
    context = {'user': user}

    if user.role == 'eleve':
        context['progressions'] = ProgressionMemorisation.objects.filter(
            eleve=user
        ).select_related('surah').order_by('-derniere_evaluation')[:5]
        context['dernieres_tentatives'] = TentativeQuiz.objects.filter(
            eleve=user
        ).select_related('quiz').order_by('-date_debut')[:5]
        context['total_sourates_memorisees'] = ProgressionMemorisation.objects.filter(
            eleve=user, statut__in=['memorise', 'maitrise']
        ).count()

    elif user.role == 'enseignant':
        classes = user.classes_principales.all()
        context['mes_classes'] = classes
        context['total_eleves'] = sum(c.eleves.count() for c in classes)
        context['derniers_bulletins'] = BulletinCoranSenegal.objects.filter(
            classe__in=classes
        ).select_related('eleve').order_by('-date_creation')[:10]

    elif user.role == 'admin':
        context['total_eleves'] = User.objects.filter(role='eleve').count()
        context['total_enseignants'] = User.objects.filter(role='enseignant').count()
        context['total_etablissements'] = Etablissement.objects.count()
        context['total_classes'] = Classe.objects.count()

    return render(request, 'accounts/tableau_de_bord.html', context)


@login_required
def profil(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.telephone = request.POST.get('telephone', user.telephone)
        if request.FILES.get('photo'):
            user.photo = request.FILES['photo']
        user.save()
        messages.success(request, "Profil mis à jour avec succès.")
        return redirect('profil')
    return render(request, 'accounts/profil.html')


@login_required
def liste_classes(request):
    if request.user.role == 'admin':
        classes = Classe.objects.select_related('etablissement', 'enseignant_principal').all()
    elif request.user.role == 'enseignant':
        classes = request.user.classes_principales.select_related('etablissement').all()
    else:
        classes = request.user.classes.select_related('etablissement').all()
    return render(request, 'accounts/classes.html', {'classes': classes})
