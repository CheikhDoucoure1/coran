from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_quiz, name='liste_quiz'),
    path('<int:pk>/', views.detail_quiz, name='detail_quiz'),
    path('<int:pk>/passer/', views.passer_quiz, name='passer_quiz'),
    path('<int:pk>/resultat/', views.resultat_quiz, name='resultat_quiz'),
    path('nouveau/', views.creer_quiz, name='creer_quiz'),
    path('<int:pk>/questions/', views.gerer_questions, name='gerer_questions'),
]
