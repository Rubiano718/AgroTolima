from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from tienda.models import Producto
from tienda.templatetags.precios import precio_colombiano

def obtener_carrito(request):
    carrito = request.session.get("carrito", {})
    if isinstance(carrito, list):
        carrito = {}
        request.session["carrito"] = carrito
    return carrito


def ver_carrito(request):
    carrito = obtener_carrito(request)
    productos = []
    total = 0

    for id_str, datos in carrito.items():
        producto = get_object_or_404(Producto, id=int(id_str))
        subtotal = datos["cantidad"] * producto.precio
        total += subtotal

        productos.append({
            "producto": producto,
            "cantidad": datos["cantidad"],
            "subtotal": subtotal,
        })

    return render(request, "carrito/carrito.html", {
        "productos": productos,
        "total": total,
    })


def agregar_carrito(request, producto_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Para comprar debes registrarte o iniciar sesion.")
        return redirect(f"{reverse('account_login')}?next={reverse('tienda:Tienda')}")

    carrito = obtener_carrito(request)
    id_str = str(producto_id)
    cantidad = int(request.POST.get("cantidad", 1))
    producto = get_object_or_404(Producto, id=producto_id)

    if not producto.disponible or producto.stock <= 0:
        messages.warning(request, "Este producto no esta disponible en este momento.")
        return redirect("tienda:Tienda")

    cantidad = max(1, min(cantidad, producto.stock))

    if id_str in carrito:
        carrito[id_str]["cantidad"] += cantidad
    else:
        carrito[id_str] = {"cantidad": cantidad}

    request.session["carrito"] = carrito
    request.session.modified = True
    return redirect("carrito:carrito")


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


def actualizar_cantidad(request, producto_id):
    if request.method != "POST":
        return redirect("carrito:carrito")

    carrito = obtener_carrito(request)
    id_str = str(producto_id)
    producto = get_object_or_404(Producto, id=producto_id)

    try:
        cantidad = int(request.POST.get("cantidad", 1))
    except (TypeError, ValueError):
        cantidad = 1

    if cantidad <= 0:
        carrito.pop(id_str, None)
        messages.success(request, f"{producto.nombre} fue eliminado del carrito.")
    else:
        cantidad = min(cantidad, producto.stock)
        carrito[id_str] = {"cantidad": cantidad}
        messages.success(request, f"Cantidad actualizada: {cantidad} unidad(es).")

    request.session["carrito"] = carrito
    request.session.modified = True
    return redirect("carrito:carrito")


def eliminar_carrito(request, producto_id):
    carrito = obtener_carrito(request)
    id_str = str(producto_id)

    if id_str in carrito:
        del carrito[id_str]

    request.session["carrito"] = carrito
    request.session.modified = True
    return redirect("carrito:carrito")


def limpiar_carrito(request):
    request.session["carrito"] = {}
    request.session.modified = True
    return redirect("carrito:carrito")


def finalizar_compra(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Para finalizar tu compra debes registrarte o iniciar sesion.")
        return redirect(f"{reverse('account_login')}?next={reverse('carrito:carrito')}")

    carrito = obtener_carrito(request)
    productos = []
    total = 0

    for id_str, datos in carrito.items():
        producto = get_object_or_404(Producto, id=int(id_str))
        subtotal = datos["cantidad"] * producto.precio
        total += subtotal

        productos.append({
            "producto": producto,
            "cantidad": datos["cantidad"],
            "subtotal": subtotal,
        })

    # ---- Generar HTML dinámico ----
    tabla = ""
    for item in productos:
        tabla += f"""
        <tr>
            <td>{item['producto'].nombre}</td>
            <td>{item['cantidad']}</td>
            <td>{precio_colombiano(item['producto'].precio)}</td>
            <td><strong>{precio_colombiano(item['subtotal'])}</strong></td>
        </tr>
        """

    html_message = f"""
    <h2 style='color:#0d6efd;'>Gracias por tu compra 🛍</h2>
    <p>Tu pedido se procesará en las próximas 24 horas.</p>

    <h3>Resumen del pedido:</h3>
    <table border='1' cellspacing='0' cellpadding='8'>
        <tr>
            <th>Producto</th>
            <th>Cantidad</th>
            <th>Precio Unidad</th>
            <th>Subtotal</th>
        </tr>
        {tabla}
    </table>

    <h3>Total pagado: <strong>{precio_colombiano(total)}</strong></h3>
    <br>
    <p>Gracias por confiar en <strong>Genesis Clothing</strong>.</p>
    """

    try:
        send_mail(
            subject="Confirmación de compra 🛒",
            message="Gracias por tu compra",   # respaldo si no soporta HTML
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            html_message=html_message,
            fail_silently=False
        )
        messages.success(request, "Compra realizada con éxito. Revisa tu correo ✔")
    except Exception as e:
        print("ERROR EN ENVÍO:", e)
        messages.success(request, "Tu pedido fue registrado. Te contactaremos para confirmar pago y entrega.")

    request.session["carrito"] = {}
    return redirect("carrito:carrito")
