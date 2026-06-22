from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Quiz, Question, ReponseQuestion, TentativeQuiz, ReponseEleve


@login_required
def liste_quiz(request):
    if request.user.role == 'eleve':
        classes = request.user.classes.all()
        quiz_list = Quiz.objects.filter(
            actif=True, classes__in=classes
        ).select_related('niveau', 'surah').distinct()
    elif request.user.role == 'enseignant':
        quiz_list = Quiz.objects.filter(
            createur=request.user
        ).select_related('niveau', 'surah')
    else:
        quiz_list = Quiz.objects.select_related('niveau', 'surah').all()

    return render(request, 'quiz/liste.html', {'quiz_list': quiz_list})


@login_required
def detail_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    tentative_existante = TentativeQuiz.objects.filter(
        eleve=request.user, quiz=quiz, statut='soumis'
    ).first() if request.user.role == 'eleve' else None

    return render(request, 'quiz/detail.html', {
        'quiz': quiz,
        'tentative_existante': tentative_existante,
        'nb_questions': quiz.questions.count(),
    })


@login_required
def passer_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    if request.user.role != 'eleve':
        messages.error(request, "Seuls les élèves peuvent passer un quiz.")
        return redirect('detail_quiz', pk=pk)

    tentative_soumise = TentativeQuiz.objects.filter(
        eleve=request.user, quiz=quiz, statut='soumis'
    ).exists()
    if tentative_soumise:
        messages.warning(request, "Vous avez déjà soumis ce quiz.")
        return redirect('resultat_quiz', pk=pk)

    tentative, _ = TentativeQuiz.objects.get_or_create(
        eleve=request.user, quiz=quiz, statut='en_cours'
    )

    if request.method == 'POST':
        questions = quiz.questions.all()
        note_totale = 0

        for question in questions:
            reponse_id = request.POST.get(f'question_{question.pk}')
            reponse_texte = request.POST.get(f'texte_{question.pk}', '')

            reponse_choisie = None
            est_correcte = False
            points = 0

            if question.type_question in ['qcm', 'vf'] and reponse_id:
                reponse_choisie = get_object_or_404(ReponseQuestion, pk=reponse_id)
                est_correcte = reponse_choisie.est_correcte
                points = float(question.points) if est_correcte else 0

            ReponseEleve.objects.update_or_create(
                tentative=tentative, question=question,
                defaults={
                    'reponse_choisie': reponse_choisie,
                    'reponse_texte': reponse_texte,
                    'est_correcte': est_correcte,
                    'points_obtenus': points,
                }
            )
            note_totale += points

        tentative.note_obtenue = note_totale
        tentative.statut = 'soumis'
        tentative.date_soumission = timezone.now()
        tentative.save()
        messages.success(request, f"Quiz soumis ! Votre note : {note_totale:.1f}/{quiz.note_maximale}")
        return redirect('resultat_quiz', pk=pk)

    questions = quiz.questions.prefetch_related('reponses').all()
    return render(request, 'quiz/passer.html', {
        'quiz': quiz,
        'questions': questions,
        'tentative': tentative,
    })


@login_required
def resultat_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    tentative = get_object_or_404(
        TentativeQuiz, eleve=request.user, quiz=quiz, statut='soumis'
    )
    reponses = tentative.reponses_eleve.select_related(
        'question', 'reponse_choisie'
    ).prefetch_related('question__reponses').all()

    return render(request, 'quiz/resultat.html', {
        'quiz': quiz,
        'tentative': tentative,
        'reponses': reponses,
    })


@login_required
def creer_quiz(request):
    if request.user.role not in ['enseignant', 'admin']:
        messages.error(request, "Permission refusée.")
        return redirect('liste_quiz')

    from curriculum.models import NiveauScolaire
    from quran.models import Surah

    if request.method == 'POST':
        quiz = Quiz.objects.create(
            titre=request.POST['titre'],
            type_quiz=request.POST['type_quiz'],
            niveau_id=request.POST['niveau'],
            surah_id=request.POST.get('surah') or None,
            description=request.POST.get('description', ''),
            duree_minutes=request.POST.get('duree_minutes', 30),
            createur=request.user,
        )
        messages.success(request, "Quiz créé ! Ajoutez maintenant les questions.")
        return redirect('gerer_questions', pk=quiz.pk)

    return render(request, 'quiz/creer.html', {
        'niveaux': NiveauScolaire.objects.all(),
        'sourates': Surah.objects.all(),
        'types': Quiz.TYPE_CHOICES,
    })


@login_required
def gerer_questions(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if quiz.createur != request.user and request.user.role != 'admin':
        messages.error(request, "Permission refusée.")
        return redirect('liste_quiz')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'ajouter_question':
            question = Question.objects.create(
                quiz=quiz,
                type_question=request.POST['type_question'],
                enonce=request.POST['enonce'],
                enonce_arabe=request.POST.get('enonce_arabe', ''),
                points=request.POST.get('points', 1),
                explication=request.POST.get('explication', ''),
                ordre=quiz.questions.count() + 1,
            )
            # Ajouter les réponses
            reponses_textes = request.POST.getlist('reponse_texte')
            correctes = request.POST.getlist('reponse_correcte')
            for i, texte in enumerate(reponses_textes):
                if texte.strip():
                    ReponseQuestion.objects.create(
                        question=question,
                        texte=texte,
                        est_correcte=str(i) in correctes,
                    )
            messages.success(request, "Question ajoutée.")

        elif action == 'publier':
            quiz.actif = True
            quiz.save()
            messages.success(request, "Quiz publié avec succès !")
            return redirect('detail_quiz', pk=pk)

    questions = quiz.questions.prefetch_related('reponses').all()
    return render(request, 'quiz/gerer_questions.html', {
        'quiz': quiz,
        'questions': questions,
        'types_question': Question.TYPE_CHOICES,
    })
