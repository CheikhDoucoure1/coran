from django.urls import path
from . import views

urlpatterns = [
    path('', views.ma_progression, name='ma_progression'),
    path('eleve/<int:eleve_id>/', views.progression_eleve, name='progression_eleve'),
    path('session/nouvelle/', views.enregistrer_session, name='enregistrer_session'),
    path('bulletins/', views.mes_bulletins, name='mes_bulletins'),
    path('classe/<int:classe_id>/', views.tableau_classe, name='tableau_classe'),
]
