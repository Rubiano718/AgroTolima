from django.urls import path

from . import views

app_name = "tienda"

urlpatterns = [

    path(
        "",
        views.tienda,
        name="Tienda"
    ),

    path(
        "categoria/<int:categoria_id>/",
        views.categoria,
        name="Categoria"
    ),

    path(
    "productor/<int:productor_id>/",
    views.perfil_productor,
    name="perfil_productor"
),
    
    path(
        "panel-productor/",
        views.panel_productor,
        name="panel_productor"
    ),

    path(
        "crear-producto/",
        views.crear_producto,
        name="crear_producto"
    ),

    path(
        "editar-producto/<int:producto_id>/",
        views.editar_producto,
        name="editar_producto"
    ),

    path(
        "eliminar-producto/<int:producto_id>/",
        views.eliminar_producto,
        name="eliminar_producto"
    ),

    path(
        "limpiar/",
        views.limpiar_imagenes
    ),
]