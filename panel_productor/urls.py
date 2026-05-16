from django.urls import path

from . import views


app_name = "panel_productor"

urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "panel-productor/",
        views.dashboard,
        name="panel_productor"
    ),

    path(
        "mis-productos/",
        views.dashboard,
        name="mis_productos"
    ),

    path(
        "pedidos/",
        views.pedidos_productor,
        name="pedidos_productor"
    ),

    path(
        "favoritos/",
        views.mis_favoritos,
        name="mis_favoritos"
    ),

    path(
        "registro/",
        views.registro_productor,
        name="registro_productor"
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
]
