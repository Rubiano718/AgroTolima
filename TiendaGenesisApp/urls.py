from django.urls import path
from TiendaGenesisApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="Inicio"),   # ESTA ES LA RUTA QUE USA BASE.HTML
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
