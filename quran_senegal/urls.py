from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Web
    path('', include('accounts.urls')),
    path('coran/', include('quran.urls')),
    path('curriculum/', include('curriculum.urls')),
    path('progression/', include('progress.urls')),
    path('evaluations/', include('quiz.urls')),
    # API REST (single router — évite le double enregistrement du convertisseur DRF)
    path('api/', include('quran_senegal.api_urls')),
    # API Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
