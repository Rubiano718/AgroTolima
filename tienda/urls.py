from django.urls import path
from . import views

app_name = "tienda"

urlpatterns = [
    path("", views.tienda, name="Tienda"),
    path("categoria/<int:categoria_id>/", views.categoria, name="Categoria"),

    # 🔥 Ruta temporal para limpiar Render
    path("limpiar/", views.limpiar_imagenes),
]
