from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_sourates, name='liste_sourates'),
    path('<int:numero>/', views.detail_sourate, name='detail_sourate'),
    path('<int:surah_numero>/verset/<int:verset_numero>/', views.detail_verset, name='detail_verset'),
    path('glossaire/', views.glossaire, name='glossaire'),
    path('tajweed/', views.tajweed_list, name='tajweed_list'),
]
