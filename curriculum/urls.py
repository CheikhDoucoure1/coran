from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_niveaux, name='liste_niveaux'),
    path('plans/', views.liste_plans_lecon, name='liste_plans_lecon'),
    path('plans/nouveau/', views.creer_plan_lecon, name='creer_plan_lecon'),
    path('plans/<int:pk>/', views.detail_plan_lecon, name='detail_plan_lecon'),
    path('ressources/', views.ressources, name='ressources'),
    path('<str:niveau_code>/', views.programme_niveau, name='programme_niveau'),
]
