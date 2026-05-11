from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from tienda.views import limpiar_imagenes

urlpatterns = [
    # HOME
    path('', include('TiendaGenesisApp.urls')),

    # ADMIN
    path('admin/', admin.site.urls),

    path(
    "mi-panel/",
    include("panel_productor.urls")
),

    # APPS
    path('tienda/', include('tienda.urls')),
    path('carrito/', include('carrito.urls')),
    path('contacto/', include('contacto.urls')),
    path('informacion/', include('informacion.urls')),

    # LOGIN / LOGOUT
    path('accounts/', include('allauth.urls')),

    # LIMPIAR IMÁGENES
    path('limpiar/', limpiar_imagenes),
]

# MEDIA FILES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)