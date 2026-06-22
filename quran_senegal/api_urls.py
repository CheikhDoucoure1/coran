from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from quran.api_views import SurahViewSet, VersetViewSet, TajweedViewSet, GlossaireViewSet
from curriculum.api_urls import NiveauViewSet, ProgrammeViewSet, PlanDeLeconViewSet
from progress.api_urls import ProgressionViewSet, SessionViewSet, BulletinViewSet
from quiz.api_urls import QuizViewSet, TentativeViewSet
from accounts.api_urls import MeView

router = DefaultRouter()
router.register('sourates', SurahViewSet, basename='surah')
router.register('versets', VersetViewSet, basename='verset')
router.register('tajweed', TajweedViewSet, basename='tajweed')
router.register('glossaire', GlossaireViewSet, basename='glossaire')
router.register('niveaux', NiveauViewSet, basename='niveau')
router.register('programmes', ProgrammeViewSet, basename='programme')
router.register('plans-lecon', PlanDeLeconViewSet, basename='plan-lecon')
router.register('progressions', ProgressionViewSet, basename='progression')
router.register('sessions-recitation', SessionViewSet, basename='session')
router.register('bulletins', BulletinViewSet, basename='bulletin')
router.register('quiz', QuizViewSet, basename='quiz')
router.register('tentatives', TentativeViewSet, basename='tentative')

urlpatterns = router.urls + [
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    path('auth/me/', MeView.as_view(), name='api_me'),
]
