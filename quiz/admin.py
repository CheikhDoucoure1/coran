from django.contrib import admin
from .models import Quiz, Question, ReponseQuestion, TentativeQuiz, ReponseEleve


class ReponseInline(admin.TabularInline):
    model = ReponseQuestion
    extra = 4
    fields = ['texte', 'texte_arabe', 'est_correcte']


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_quiz', 'niveau', 'surah', 'duree_minutes', 'actif', 'createur']
    list_filter = ['type_quiz', 'actif', 'niveau']
    search_fields = ['titre']
    raw_id_fields = ['surah', 'createur']
    filter_horizontal = ['classes']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['enonce', 'type_question', 'quiz', 'points', 'ordre']
    list_filter = ['type_question', 'quiz']
    inlines = [ReponseInline]


@admin.register(TentativeQuiz)
class TentativeAdmin(admin.ModelAdmin):
    list_display = ['eleve', 'quiz', 'statut', 'note_obtenue', 'date_soumission']
    list_filter = ['statut', 'quiz']
    search_fields = ['eleve__username', 'eleve__last_name']
    raw_id_fields = ['eleve']
