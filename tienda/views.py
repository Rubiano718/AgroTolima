from django.db.models import Q
from django.contrib import messages
from carrito.models import PedidoItem
from django.db.models import Sum
from carrito.models import Pedido
from .models import Resena
from .forms import ResenaForm
from .models import Favorito
from django.shortcuts import (

    render,
    get_object_or_404,
    redirect
)

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from tienda.models import (
    Producto,
    CategoriaProducto,
    Productor
)

from .forms import ProductoForm


# =====================================================
# TIENDA
# =====================================================

def tienda(request):

    productos = Producto.objects.select_related(
        "categoria",
        "productor"
    ).all()

    categorias = CategoriaProducto.objects.all()

    productores = Productor.objects.all()

    busqueda = request.GET.get(
        "q",
        ""
    ).strip()

    categoria_id = request.GET.get(
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

    if busqueda:

        productos = productos.filter(

            Q(nombre__icontains=busqueda)
            | Q(descripcion__icontains=busqueda)
            | Q(categoria__nombre__icontains=busqueda)
            | Q(productor__nombre__icontains=busqueda)
            | Q(productor__municipio__icontains=busqueda)

        )

    if categoria_id:

        productos = productos.filter(
            categoria_id=categoria_id
        )

    if productor_id:

        productos = productos.filter(
            productor_id=productor_id
        )

    if precio_min:

        productos = productos.filter(
            precio__gte=precio_min
        )

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
            "categoria": categoria_id,
            "productor": productor_id,
            "precio_min": precio_min,
            "precio_max": precio_max,

        }

    })


# =====================================================
# CATEGORÍAS
# =====================================================

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

# =====================================================
# PERFIL PÚBLICO PRODUCTOR
# =====================================================

def perfil_productor(request, productor_id):

    productor = get_object_or_404(
        Productor,
        id=productor_id
    )

    productos = Producto.objects.filter(
        productor=productor
    )

    return render(
        request,
        "tienda/perfil_productor.html",
        {
            "productor": productor,
            "productos": productos
        }
    ) 

# =====================================================
# PANEL PRODUCTOR
# =====================================================

@login_required
def panel_productor(request):

    if not hasattr(request.user, "productor"):
        messages.warning(
            request,
            "Debes registrarte como productor antes de publicar productos."
        )
        return redirect("/mi-panel/registro/")

    productor = request.user.productor

    productos = Producto.objects.filter(
        productor=productor
    )

    return render(
        request,
        "tienda/panel_productor.html",
        {
            "productor": productor,
            "productos": productos
        }
    )


# =====================================================
# CREAR PRODUCTO
# =====================================================

@login_required
def crear_producto(request):

    if not hasattr(request.user, "productor"):
        messages.warning(
            request,
            "Debes registrarte como productor antes de publicar productos."
        )
        return redirect("/mi-panel/registro/")

    productor = request.user.productor

    if request.method == "POST":

        form = ProductoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            producto = form.save(commit=False)

            producto.productor = productor

            producto.save()

            messages.success(
                request,
                "Producto publicado correctamente."
            )

            return redirect(
                "tienda:panel_productor"
            )
        else:
            messages.warning(
                request,
                "Completa todos los campos obligatorios."
            )

    else:

        form = ProductoForm()

    return render(
        request,
        "tienda/crear_producto.html",
        {
            "form": form
        }
    )


# =====================================================
# EDITAR PRODUCTO
# =====================================================

@login_required
def editar_producto(request, producto_id):

    if not hasattr(request.user, "productor"):
        messages.warning(
            request,
            "Debes registrarte como productor antes de publicar productos."
        )
        return redirect("/mi-panel/registro/")

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    if producto.productor.usuario != request.user:
        return redirect("tienda:panel_productor")

    if request.method == "POST":

        form = ProductoForm(
            request.POST,
            request.FILES,
            instance=producto
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Producto actualizado correctamente."
            )

            return redirect(
                "tienda:panel_productor"
            )
        else:
            messages.warning(
                request,
                "Completa todos los campos obligatorios."
            )

    else:

        form = ProductoForm(instance=producto)

    return render(
        request,
        "tienda/crear_producto.html",
        {
            "form": form
        }
    )


# =====================================================
# ELIMINAR PRODUCTO
# =====================================================

@login_required
def eliminar_producto(request, producto_id):

    if not hasattr(request.user, "productor"):
        messages.warning(
            request,
            "Debes registrarte como productor antes de publicar productos."
        )
        return redirect("/mi-panel/registro/")

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    if producto.productor.usuario == request.user:
        producto.delete()
        messages.success(
            request,
            "Producto eliminado correctamente."
        )

    return redirect("tienda:panel_productor")


# =====================================================
# LIMPIAR IMÁGENES
# =====================================================

def limpiar_imagenes(request):

    productos = Producto.objects.all()

    count = 0

    for p in productos:

        if p.imagen and "tienda/" in p.imagen:

            p.imagen = p.imagen.replace(
                "tienda/",
                ""
            )

            p.save()

            count += 1

    return HttpResponse(
        f"Rutas corregidas: {count}"
    )

# =====================================================
# PEDIDOS PRODUCTOR
# =====================================================

@login_required
def pedidos_productor(request):

    if not hasattr(request.user, "productor"):
        messages.warning(
            request,
            "Debes registrarte como productor antes de revisar ventas."
        )
        return redirect("/mi-panel/registro/")

    productor = request.user.productor

    pedidos = PedidoItem.objects.filter(
        producto__productor=productor
    ).select_related(
        "pedido",
        "producto"
    ).order_by("-pedido__creado")

    total_ventas = pedidos.aggregate(
        total=Sum("subtotal")
    )["total"] or 0

    total_productos = Producto.objects.filter(
        productor=productor
    ).count()

    total_pedidos = pedidos.count()

    return render(
        request,
        "tienda/pedidos_productor.html",
        {
            "productor": productor,
            "pedidos": pedidos,
            "total_ventas": total_ventas,
            "total_productos": total_productos,
            "total_pedidos": total_pedidos,
        }
    )


# =====================================================
# ACTUALIZAR ESTADO PEDIDO
# =====================================================

@login_required
def actualizar_estado_pedido(
    request,
    pedido_id,
    estado
):

    if not hasattr(request.user, "productor"):
        messages.warning(
            request,
            "Debes registrarte como productor antes de gestionar pedidos."
        )
        return redirect("/mi-panel/registro/")

    productor = request.user.productor

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id
    )

    productos_productor = pedido.items.filter(
        producto__productor=productor
    )

    if not productos_productor.exists():
        messages.warning(
            request,
            "No tienes permiso para modificar este pedido."
        )

        return redirect(
            "tienda:pedidos_productor"
        )

    estados_validos = [
        "recibido",
        "confirmado",
        "enviado",
        "entregado"
    ]

    if estado in estados_validos:

        pedido.estado = estado

        pedido.save()

        messages.success(
            request,
            "Estado del pedido actualizado correctamente."
        )
    else:
        messages.warning(
            request,
            "Estado de pedido no valido."
        )

    return redirect(
        "tienda:pedidos_productor"
    )
# =====================================================
# DETALLE PRODUCTO
# =====================================================

def detalle_producto(request, producto_id):

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    relacionados = Producto.objects.filter(
        categoria=producto.categoria
    ).exclude(
        id=producto.id
    )[:4]

    resenas = producto.resenas.all().order_by(
        "-creado"
    )

    if request.method == "POST":

        if request.user.is_authenticated:

            form = ResenaForm(request.POST)

            if form.is_valid():

                resena = form.save(commit=False)

                resena.producto = producto

                resena.usuario = request.user

                resena.save()

                messages.success(
                    request,
                    "Gracias por compartir tu opinion."
                )

                return redirect(
                    "tienda:detalle_producto",
                    producto.id
                )

        else:

            return redirect("account_login")

    else:

        form = ResenaForm()

    es_favorito = False

    if request.user.is_authenticated:

        es_favorito = Favorito.objects.filter(
            usuario=request.user,
            producto=producto
        ).exists()

    return render(
        request,
        "tienda/detalle_producto.html",
        {
            "producto": producto,
            "relacionados": relacionados,
            "resenas": resenas,
            "form": form,
            "es_favorito": es_favorito
        }
    )
@login_required
def toggle_favorito(request, producto_id):

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    favorito = Favorito.objects.filter(
        usuario=request.user,
        producto=producto
    )

    if favorito.exists():

        favorito.delete()
        messages.info(
            request,
            "Este producto ya esta en favoritos. Lo retiramos de tu lista."
        )

    else:

        Favorito.objects.create(
            usuario=request.user,
            producto=producto
        )
        messages.success(
            request,
            "Producto agregado a favoritos."
        )

    return redirect(
        "tienda:detalle_producto",
        producto.id
    )


@login_required
def mis_favoritos(request):

    favoritos = Favorito.objects.filter(
        usuario=request.user
    ).select_related(
        "producto",
        "producto__productor"
    ).order_by("-creado")

    return render(
        request,
        "tienda/mis_favoritos.html",
        {
            "favoritos": favoritos
        }
    )
