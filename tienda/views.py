from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from tienda.models import (
    Producto,
    CategoriaProducto,
    Productor
)


# -----------------------------
# 🔹 Vista principal de tienda
# -----------------------------
def tienda(request):

    productos = Producto.objects.select_related(
        "categoria",
        "productor"
    ).all()

    categorias = CategoriaProducto.objects.all()
    productores = Productor.objects.all()

    # FILTROS

    busqueda = request.GET.get(
        "q",
        ""
    ).strip()

    categoria_nombre = request.GET.get(
        "categoria",
        ""
    ).strip()

    productor_id = request.GET.get(
        "productor",
        ""
    ).strip()

    precio_min = request.GET.get(
        "precio_min",
        ""
    ).strip()

    precio_max = request.GET.get(
        "precio_max",
        ""
    ).strip()

    # BUSCADOR GENERAL

    if busqueda:

        productos = productos.filter(

            Q(nombre__icontains=busqueda)
            | Q(descripcion__icontains=busqueda)
            | Q(categoria__nombre__icontains=busqueda)
            | Q(productor__nombre__icontains=busqueda)
            | Q(productor__municipio__icontains=busqueda)

        )

    # FILTRO POR CATEGORÍA

    if categoria_nombre:

        productos = productos.filter(
            categoria__nombre__icontains=categoria_nombre
        )

    # FILTRO POR PRODUCTOR

    if productor_id:

        productos = productos.filter(
            productor_id=productor_id
        )

    # FILTRO PRECIO MÍNIMO

    if precio_min:

        productos = productos.filter(
            precio__gte=precio_min
        )

    # FILTRO PRECIO MÁXIMO

    if precio_max:

        productos = productos.filter(
            precio__lte=precio_max
        )

    return render(request, "tienda/tienda.html", {

        "productos": productos,
        "categorias": categorias,
        "productores": productores,

        "filtros": {

            "q": busqueda,
            "categoria": categoria_nombre,
            "productor": productor_id,
            "precio_min": precio_min,
            "precio_max": precio_max,

        }

    })


# -----------------------------
# 🔹 Vista de productos por categoría
# -----------------------------
def categoria(request, categoria_id):

    categoria = get_object_or_404(
        CategoriaProducto,
        id=categoria_id
    )

    productos = Producto.objects.select_related(
        "categoria",
        "productor"
    ).filter(categoria=categoria)

    categorias = CategoriaProducto.objects.all()

    return render(request, "tienda/categorias.html", {

        "categoria": categoria,
        "productos": productos,
        "categorias": categorias

    })


# ---------------------------------------------------------
# 🔥 Vista temporal para limpiar rutas antiguas del campo imagen
# ---------------------------------------------------------
def limpiar_imagenes(request):

    productos = Producto.objects.all()

    count = 0

    for p in productos:

        if p.imagen and "tienda/" in p.imagen:

            # Eliminar prefijo antiguo
            p.imagen = p.imagen.replace("tienda/", "")

            p.save()

            count += 1

    return HttpResponse(
        f"Rutas corregidas: {count}"
    )



