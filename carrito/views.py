from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from tienda.models import Producto
from tienda.templatetags.precios import precio_colombiano

from .forms import CheckoutForm
from .models import Pedido, PedidoItem


# =====================================================
# OBTENER CARRITO
# =====================================================

def obtener_carrito(request):

    carrito = request.session.get("carrito", {})

    if isinstance(carrito, list):

        carrito = {}

        request.session["carrito"] = carrito

    return carrito


# =====================================================
# VER CARRITO
# =====================================================

def ver_carrito(request):

    carrito = obtener_carrito(request)

    productos = []

    total = 0

    for id_str, datos in carrito.items():

        producto = get_object_or_404(
            Producto,
            id=int(id_str)
        )

        subtotal = datos["cantidad"] * producto.precio

        total += subtotal

        productos.append({

            "producto": producto,

            "cantidad": datos["cantidad"],

            "subtotal": subtotal,

        })

    return render(
        request,
        "carrito/carrito.html",
        {
            "productos": productos,
            "total": total,
        }
    )


# =====================================================
# AGREGAR AL CARRITO
# =====================================================

def agregar_carrito(request, producto_id):

    if not request.user.is_authenticated:

        messages.warning(
            request,
            "Para comprar debes registrarte o iniciar sesion."
        )

        return redirect(
            f"{reverse('account_login')}?next={reverse('tienda:Tienda')}"
        )

    carrito = obtener_carrito(request)

    id_str = str(producto_id)

    cantidad = int(
        request.POST.get("cantidad", 1)
    )

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    if not producto.disponible or producto.stock <= 0:

        messages.warning(
            request,
            "Este producto no esta disponible en este momento."
        )

        return redirect("tienda:Tienda")

    cantidad = max(
        1,
        min(cantidad, producto.stock)
    )

    if id_str in carrito:

        carrito[id_str]["cantidad"] += cantidad

    else:

        carrito[id_str] = {
            "cantidad": cantidad
        }

    request.session["carrito"] = carrito

    request.session.modified = True

    return redirect("carrito:carrito")


# =====================================================
# RESTAR CARRITO
# =====================================================

def restar_carrito(request, producto_id):

    carrito = obtener_carrito(request)

    id_str = str(producto_id)

    if id_str in carrito:

        carrito[id_str]["cantidad"] -= 1

        if carrito[id_str]["cantidad"] <= 0:

            del carrito[id_str]

    request.session["carrito"] = carrito

    request.session.modified = True

    return redirect("carrito:carrito")


# =====================================================
# ACTUALIZAR CANTIDAD
# =====================================================

def actualizar_cantidad(request, producto_id):

    if request.method != "POST":

        return redirect("carrito:carrito")

    carrito = obtener_carrito(request)

    id_str = str(producto_id)

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    try:

        cantidad = int(
            request.POST.get("cantidad", 1)
        )

    except (TypeError, ValueError):

        cantidad = 1

    if cantidad <= 0:

        carrito.pop(id_str, None)

        messages.success(
            request,
            f"{producto.nombre} fue eliminado del carrito."
        )

    else:

        cantidad = min(
            cantidad,
            producto.stock
        )

        carrito[id_str] = {
            "cantidad": cantidad
        }

        messages.success(
            request,
            f"Cantidad actualizada: {cantidad} unidad(es)."
        )

    request.session["carrito"] = carrito

    request.session.modified = True

    return redirect("carrito:carrito")


# =====================================================
# ELIMINAR CARRITO
# =====================================================

def eliminar_carrito(request, producto_id):

    carrito = obtener_carrito(request)

    id_str = str(producto_id)

    if id_str in carrito:

        del carrito[id_str]

    request.session["carrito"] = carrito

    request.session.modified = True

    return redirect("carrito:carrito")


# =====================================================
# LIMPIAR CARRITO
# =====================================================

def limpiar_carrito(request):

    request.session["carrito"] = {}

    request.session.modified = True

    return redirect("carrito:carrito")


# =====================================================
# CHECKOUT
# =====================================================

@login_required
def checkout(request):

    carrito = obtener_carrito(request)

    productos = []

    total = Decimal("0.00")

    for id_str, datos in carrito.items():

        producto = get_object_or_404(
            Producto,
            id=int(id_str)
        )

        subtotal = datos["cantidad"] * producto.precio

        total += subtotal

        productos.append({

            "producto": producto,

            "cantidad": datos["cantidad"],

            "subtotal": subtotal,

        })

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            pedido = Pedido.objects.create(

                usuario=request.user,

                nombre=form.cleaned_data["nombre"],

                correo=form.cleaned_data["correo"],

                telefono=form.cleaned_data["telefono"],

                ciudad=form.cleaned_data["ciudad"],

                direccion=form.cleaned_data["direccion"],

                total=total

            )

            # =========================
            # GUARDAR PRODUCTOS PEDIDO
            # =========================

            for item in productos:

                PedidoItem.objects.create(

                    pedido=pedido,

                    producto=item["producto"],

                    cantidad=item["cantidad"],

                    precio=item["producto"].precio,

                    subtotal=item["subtotal"]

                )

            # =========================
            # EMAIL HTML
            # =========================

            productos_html = ""

            for item in productos:

                productos_html += f"""
                <tr>
                    <td>{item['producto'].nombre}</td>
                    <td>{item['cantidad']}</td>
                    <td>{precio_colombiano(item['subtotal'])}</td>
                </tr>
                """

            html_message = f"""
            <h2 style="color:#198754;">
                Gracias por comprar en AgroTolima 🌱
            </h2>

            <p>
                Tu pedido fue registrado correctamente.
            </p>

            <h3>Resumen del pedido:</h3>

            <table border="1"
                   cellpadding="10"
                   cellspacing="0"
                   style="border-collapse:collapse;">

                <tr>
                    <th>Producto</th>
                    <th>Cantidad</th>
                    <th>Subtotal</th>
                </tr>

                {productos_html}

            </table>

            <h3>
                Total:
                {precio_colombiano(total)}
            </h3>

            <p>
                El productor confirmará tu pedido pronto.
            </p>

            <br>

            <p>
                Gracias por apoyar productores regionales ❤️
            </p>
            """

            # =========================
            # ENVIAR EMAIL
            # =========================

            try:

                send_mail(

                    subject="Confirmación de pedido AgroTolima",

                    message="Tu pedido fue registrado correctamente",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[pedido.correo],

                    html_message=html_message,

                    fail_silently=False

                )

            except Exception as e:

                print("ERROR EMAIL:", e)

            # =========================
            # LIMPIAR CARRITO
            # =========================

            request.session["carrito"] = {}

            request.session.modified = True

            messages.success(
                request,
                "Pedido realizado correctamente"
            )

            return render(
                request,
                "carrito/compra_exitosa.html",
                {
                    "pedido": pedido
                }
            )

    else:

        initial_data = {

    "nombre": request.user.email,

    "correo": request.user.email,

}

        form = CheckoutForm(
            initial=initial_data
        )

    return render(

        request,

        "carrito/checkout.html",

        {

            "form": form,

            "productos": productos,

            "total": total

        }

    )


# =====================================================
# MIS PEDIDOS
# =====================================================

@login_required
def mis_pedidos(request):

    pedidos = Pedido.objects.filter(
        usuario=request.user
    ).order_by("-creado")

    return render(
        request,
        "carrito/mis_pedidos.html",
        {
            "pedidos": pedidos
        }
    )