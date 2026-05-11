from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from tienda.models import (
    Productor,
    Producto
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

            return redirect(
                "panel_productor:dashboard"
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
        return redirect(
            "panel_productor:registro_productor"
        )

    productor = request.user.productor

    productos = Producto.objects.filter(
        productor=productor
    )

    return render(
        request,
        "panel_productor/dashboard.html",
        {
            "productor": productor,
            "productos": productos,
        }
    )


# ==================================================
# CREAR PRODUCTO
# ==================================================

@login_required
def crear_producto(request):

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

            return redirect(
                "panel_productor:dashboard"
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

            return redirect(
                "panel_productor:dashboard"
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

    productor = request.user.productor

    producto = get_object_or_404(
        Producto,
        id=producto_id,
        productor=productor
    )

    if request.method == "POST":

        producto.delete()

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