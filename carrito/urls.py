from django.urls import path
from . import views

app_name = "carrito"

urlpatterns = [

    path('', views.ver_carrito, name="carrito"),

    path(
        'agregar/<int:producto_id>/',
        views.agregar_carrito,
        name="agregar_carrito"
    ),

    path(
        'actualizar/<int:producto_id>/',
        views.actualizar_cantidad,
        name="actualizar_cantidad"
    ),

    path(
        'restar/<int:producto_id>/',
        views.restar_carrito,
        name="restar_carrito"
    ),

    path(
        'eliminar/<int:producto_id>/',
        views.eliminar_carrito,
        name="eliminar_carrito"
    ),

    path(
        'limpiar/',
        views.limpiar_carrito,
        name="limpiar_carrito"
    ),

    path(
        'finalizar/',
        views.finalizar_compra,
        name="finalizar"
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),
    path(
    "mis-pedidos/",
    views.mis_pedidos,
    name="mis_pedidos"
),
path(
    "mis-pedidos/",
    views.mis_pedidos,
    name="mis_pedidos"
),

]