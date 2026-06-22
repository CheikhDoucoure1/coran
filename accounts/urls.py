from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('accounts/connexion/', views.connexion, name='connexion'),
    path('accounts/deconnexion/', views.deconnexion, name='deconnexion'),
    path('accounts/inscription/', views.inscription_etablissement, name='inscription_etablissement'),
    path('tableau-de-bord/', views.tableau_de_bord, name='tableau_de_bord'),
    path('profil/', views.profil, name='profil'),
    path('classes/', views.liste_classes, name='liste_classes'),
]
