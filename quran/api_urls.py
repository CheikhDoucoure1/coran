from rest_framework.routers import DefaultRouter
from .api_views import SurahViewSet, VersetViewSet, TajweedViewSet, GlossaireViewSet

router = DefaultRouter()
router.register('sourates', SurahViewSet, basename='surah')
router.register('versets', VersetViewSet, basename='verset')
router.register('tajweed', TajweedViewSet, basename='tajweed')
router.register('glossaire', GlossaireViewSet, basename='glossaire')

urlpatterns = router.urls
