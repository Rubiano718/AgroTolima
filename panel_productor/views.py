from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from carrito.models import (
    Pedido,
    PedidoItem
)

from tienda.models import (
    Producto,
    CategoriaProducto,
    Productor,
    ProductoImagen,
    Favorito
)

from .forms import (
    RegistroProductorForm,
    ProductoProductorForm
)


# ==================================================
# REGISTRO PRODUCTOR
# ==================================================

@login_required
def registro_productor(request):

    if hasattr(request.user, "productor"):
        messages.info(
            request,
            "Ya tienes un perfil de productor activo."
        )
        return redirect("panel_productor:dashboard")

    form = RegistroProductorForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST":

        if form.is_valid():

            productor = form.save(commit=False)

            productor.usuario = request.user

            productor.save()

            messages.success(
                request,
                "Perfil de productor creado correctamente."
            )

            return redirect(
                "panel_productor:dashboard"
            )
        else:
            messages.warning(
                request,
                "Completa todos los campos obligatorios."
            )

    return render(
        request,
        "panel_productor/registro_productor.html",
        {
            "form": form
        }
    )


# ==================================================
# DASHBOARD
# ==================================================

@login_required
def dashboard(request):

    if not hasattr(request.user, "productor"):
        messages.warning(
            request,
            "Debes registrarte como productor antes de publicar productos."
        )
        return redirect(
            "panel_productor:registro_productor"
        )

    productor = request.user.productor

    productos = Producto.objects.filter(
        productor=productor
    )

    pedidos_items = PedidoItem.objects.filter(
        producto__productor=productor
    ).select_related(
        "pedido",
        "producto",
        "pedido__usuario"
    ).order_by("-pedido__creado")

    total_ventas = pedidos_items.aggregate(
        total=Sum("subtotal")
    )["total"] or 0

    total_pedidos = Pedido.objects.filter(
        items__producto__productor=productor
    ).distinct().count()

    productos_favoritos = Favorito.objects.filter(
        producto__productor=productor
    ).count()

    productos_mas_vendidos = productos.annotate(
        unidades_vendidas=Sum("pedidoitem__cantidad"),
        ingresos_generados=Sum("pedidoitem__subtotal")
    ).order_by(
        "-unidades_vendidas",
        "-created"
    )[:5]

    return render(
        request,
        "panel_productor/dashboard.html",
        {
            "productor": productor,
            "productos": productos,
            "total_ventas": total_ventas,
            "total_pedidos": total_pedidos,
            "total_productos": productos.count(),
            "productos_favoritos": productos_favoritos,
            "ganancias_estimadas": total_ventas,
            "productos_mas_vendidos": productos_mas_vendidos,
            "ultimos_pedidos": pedidos_items[:8],
        }
    )


@login_required
def pedidos_productor(request):

    if not hasattr(request.user, "productor"):
        messages.warning(
            request,
            "Debes registrarte como productor antes de revisar ventas."
        )
        return redirect(
            "panel_productor:registro_productor"
        )

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

    total_pedidos = Pedido.objects.filter(
        items__producto__productor=productor
    ).distinct().count()

    total_productos = Producto.objects.filter(
        productor=productor
    ).count()

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


@login_required
def mis_favoritos(request):

    if not hasattr(request.user, "productor"):
        messages.warning(
            request,
            "Debes registrarte como productor antes de ver favoritos."
        )
        return redirect(
            "panel_productor:registro_productor"
        )

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


# ==================================================
# CREAR PRODUCTO
# ==================================================

@login_required
def crear_producto(request):

    if not hasattr(request.user, "productor"):
        messages.warning(
            request,
            "Debes registrarte como productor antes de publicar productos."
        )
        return redirect(
            "panel_productor:registro_productor"
        )

    productor = request.user.productor

    form = ProductoProductorForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST":

        if form.is_valid():

            producto = form.save(commit=False)

            producto.productor = productor

            producto.save()

            messages.success(
                request,
                "Producto publicado correctamente."
            )

            return redirect(
                "panel_productor:dashboard"
            )
        else:
            messages.warning(
                request,
                "Completa todos los campos obligatorios."
            )

    return render(
        request,
        "panel_productor/producto_form.html",
        {
            "form": form,
            "titulo": "Agregar producto"
        }
    )


# ==================================================
# EDITAR PRODUCTO
# ==================================================

@login_required
def editar_producto(request, producto_id):

    if not hasattr(request.user, "productor"):
        messages.warning(
            request,
            "Debes registrarte como productor antes de editar productos."
        )
        return redirect(
            "panel_productor:registro_productor"
        )

    productor = request.user.productor

    producto = get_object_or_404(
        Producto,
        id=producto_id,
        productor=productor
    )

    form = ProductoProductorForm(
        request.POST or None,
        request.FILES or None,
        instance=producto
    )

    if request.method == "POST":

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Producto actualizado correctamente."
            )

            return redirect(
                "panel_productor:dashboard"
            )
        else:
            messages.warning(
                request,
                "Completa todos los campos obligatorios."
            )

    return render(
        request,
        "panel_productor/producto_form.html",
        {
            "form": form,
            "titulo": "Editar producto"
        }
    )


# ==================================================
# ELIMINAR PRODUCTO
# ==================================================

@login_required
def eliminar_producto(request, producto_id):

    if not hasattr(request.user, "productor"):
        messages.warning(
            request,
            "Debes registrarte como productor antes de eliminar productos."
        )
        return redirect(
            "panel_productor:registro_productor"
        )

    productor = request.user.productor

    producto = get_object_or_404(
        Producto,
        id=producto_id,
        productor=productor
    )

    if request.method == "POST":

        producto.delete()

        messages.success(
            request,
            "Producto eliminado correctamente."
        )

        return redirect(
            "panel_productor:dashboard"
        )

    return render(
        request,
        "panel_productor/eliminar_producto.html",
        {
            "producto": producto
        }
    )
