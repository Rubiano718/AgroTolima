from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
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

    try:
        cantidad = int(
            request.POST.get("cantidad", 1) or 1
        )
    except (TypeError, ValueError):
        cantidad = 1

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

    cantidad_actual = carrito.get(id_str, {}).get("cantidad", 0)
    cantidad_solicitada = cantidad_actual + max(1, cantidad)

    if cantidad_solicitada > producto.stock:
        messages.warning(
            request,
            "La cantidad supera el stock disponible."
        )
        return redirect("carrito:carrito")

    if id_str in carrito:

        carrito[id_str]["cantidad"] = cantidad_solicitada

    else:

        carrito[id_str] = {
            "cantidad": max(1, cantidad)
        }

    request.session["carrito"] = carrito

    request.session.modified = True

    messages.success(
        request,
        f"{producto.nombre_con_unidad} agregado al carrito."
    )

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

        if cantidad > producto.stock:
            messages.warning(
                request,
                "La cantidad supera el stock disponible."
            )
            return redirect("carrito:carrito")

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

    if not carrito:
        messages.warning(
            request,
            "Tu carrito esta vacio."
        )
        return redirect("carrito:carrito")

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

    if not carrito:
        messages.warning(
            request,
            "Tu carrito esta vacio."
        )
        return redirect("carrito:carrito")

    productos = []

    total = Decimal("0.00")

    for id_str, datos in carrito.items():

        producto = get_object_or_404(
            Producto,
            id=int(id_str)
        )

        if datos["cantidad"] > producto.stock:
            messages.warning(
                request,
                "La cantidad supera el stock disponible."
            )
            return redirect("carrito:carrito")

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

            with transaction.atomic():

                productos_bloqueados = []

                for item in productos:
                    producto = Producto.objects.select_for_update().get(
                        id=item["producto"].id
                    )

                    if item["cantidad"] > producto.stock:
                        messages.warning(
                            request,
                            "La cantidad supera el stock disponible."
                        )
                        return redirect("carrito:carrito")

                    productos_bloqueados.append(
                        {
                            "producto": producto,
                            "cantidad": item["cantidad"],
                            "subtotal": item["subtotal"],
                        }
                    )

                pedido = Pedido.objects.create(

    usuario=request.user,

    nombre=form.cleaned_data["nombre"],

    correo=form.cleaned_data["correo"],

    telefono=form.cleaned_data["telefono"],

    departamento=form.cleaned_data["departamento"],

    municipio=form.cleaned_data["municipio"],

    direccion=form.cleaned_data["direccion"],

    informacion_adicional=form.cleaned_data["informacion_adicional"],

    total=total

)

            # =========================
            # GUARDAR PRODUCTOS PEDIDO
            # =========================

                for item in productos_bloqueados:

                    PedidoItem.objects.create(

                        pedido=pedido,

                        producto=item["producto"],

                        cantidad=item["cantidad"],

                        precio=item["producto"].precio,

                        subtotal=item["subtotal"]

                    )

                    item["producto"].stock -= item["cantidad"]
                    item["producto"].disponible = item["producto"].stock > 0
                    item["producto"].save(
                        update_fields=["stock", "disponible"]
                    )

                productos = productos_bloqueados

            # =========================
            # EMAIL HTML
            # =========================
# =========================
# EMAIL HTML CLIENTE
# =========================

            productos_html = ""

            for item in productos:

                imagen_producto = ""

                if item["producto"].imagen:

                    imagen_producto = f"""
                    <img src="{item['producto'].imagen.url}"
                         width="70"
                         style="border-radius:12px;
                                object-fit:cover;">
                    """

                productos_html += f"""
                <tr>
                    <td style="padding:12px;">
                        {imagen_producto}
                    </td>

                    <td style="padding:12px;">
                        <strong>
                            {item['producto'].nombre}
                        </strong>
                        <br>
                        <small>
                            {item['producto'].nombre_con_unidad}
                        </small>
                    </td>

                    <td style="padding:12px;text-align:center;">
                        {item['cantidad']}
                    </td>

                    <td style="padding:12px;text-align:right;">
                        {precio_colombiano(item['subtotal'])}
                    </td>
                </tr>
                """

            html_message = f"""
            <div style="
                font-family:Arial,sans-serif;
                max-width:700px;
                margin:auto;
                background:#ffffff;
                border-radius:18px;
                overflow:hidden;
                border:1px solid #eaeaea;
            ">

                <div style="
                    background:#198754;
                    padding:35px;
                    text-align:center;
                    color:white;
                ">

                    <h1 style="margin:0;">
                        Pedido confirmado
                    </h1>

                    <p style="margin-top:10px;font-size:16px;">
                        Gracias por comprar en AgroTolima
                    </p>

                </div>

                <div style="padding:35px;">

                    <h2 style="margin-top:0;">
                        Hola {pedido.nombre}
                    </h2>

                    <p style="
                        color:#555;
                        line-height:1.7;
                    ">
                        Tu pedido fue registrado correctamente y ya fue enviado
                        a los productores regionales.
                    </p>

                    <div style="
                        background:#f8f9fa;
                        padding:20px;
                        border-radius:14px;
                        margin:25px 0;
                    ">

                        <h3 style="margin-top:0;">
                            Información de entrega
                        </h3>

                        <p>
                            <strong>Correo:</strong>
                            {pedido.correo}
                        </p>

                        <p>
                            <strong>Teléfono:</strong>
                            {pedido.telefono}
                        </p>

                        <p>
                            <strong>Departamento:</strong>
                            {pedido.departamento}
                        </p>

                        <p>
                            <strong>Municipio:</strong>
                            {pedido.municipio}
                        </p>

                        <p>
                            <strong>Dirección:</strong>
                            {pedido.direccion}
                        </p>

                        <p>
                            <strong>Información adicional:</strong>
                            {pedido.informacion_adicional or 'No especificada'}
                        </p>

                    </div>

                    <h3>
                        Productos comprados
                    </h3>

                    <table width="100%"
                           style="
                           border-collapse:collapse;
                           margin-top:20px;
                           ">

                        <thead>

                            <tr style="
                                background:#198754;
                                color:white;
                            ">

                                <th style="padding:14px;">
                                    Imagen
                                </th>

                                <th style="padding:14px;">
                                    Producto
                                </th>

                                <th style="padding:14px;">
                                    Cantidad
                                </th>

                                <th style="padding:14px;">
                                    Subtotal
                                </th>

                            </tr>

                        </thead>

                        <tbody>

                            {productos_html}

                        </tbody>

                    </table>

                    <div style="
                        margin-top:30px;
                        padding:25px;
                        background:#f1fff6;
                        border-radius:14px;
                    ">

                        <h2 style="
                            margin:0;
                            color:#198754;
                        ">
                            Total:
                            {precio_colombiano(total)}
                        </h2>

                    </div>

                    <p style="
                        margin-top:30px;
                        color:#666;
                        line-height:1.7;
                    ">
                        El productor confirmará tu pedido pronto.
                        Recibirás novedades directamente desde AgroTolima.
                    </p>

                </div>

                <div style="
                    background:#f8f9fa;
                    padding:25px;
                    text-align:center;
                    color:#777;
                    font-size:14px;
                ">

                    © AgroTolima Marketplace Regional

                </div>

            </div>
            """

            # =========================
            # ENVIAR EMAIL CLIENTE
            # =========================

            try:

                send_mail(

                    subject="Pedido confirmado - AgroTolima",

                    message="Tu pedido fue registrado correctamente.",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[pedido.correo],

                    html_message=html_message,

                    fail_silently=False

                )

            except Exception as e:

                print("ERROR EMAIL CLIENTE:", e)

            # =========================
            # EMAIL PRODUCTORES
            # =========================

            productores_notificados = set()

            for item in productos:

                productor = item["producto"].productor

                if (
                    not productor.correo
                    or productor.correo in productores_notificados
                ):
                    continue

                productos_productor = [
                    p for p in productos
                    if p["producto"].productor == productor
                ]

                productos_html_productor = ""

                for p in productos_productor:

                    productos_html_productor += f"""
                    <tr>
                        <td>{p['producto'].nombre}</td>
                        <td>{p['cantidad']}</td>
                        <td>{precio_colombiano(p['subtotal'])}</td>
                    </tr>
                    """

                html_productor = f"""
                <h2 style="color:#198754;">
                    Nuevo pedido recibido
                </h2>

                <p>
                    Hola {productor.nombre}, tienes una nueva compra en AgroTolima.
                </p>

                <h3>Datos del comprador</h3>

                <ul>
                    <li><strong>Nombre:</strong> {pedido.nombre}</li>
                    <li><strong>Correo:</strong> {pedido.correo}</li>
                    <li><strong>Telefono:</strong> {pedido.telefono}</li>
                    <li><strong>Departamento:</strong> {pedido.departamento}</li>
                    <li><strong>Municipio:</strong> {pedido.municipio}</li>
                    <li><strong>Direccion:</strong> {pedido.direccion}</li>
                    <li><strong>Informacion adicional:</strong> {pedido.informacion_adicional or 'No especificada'}</li>
                </ul>

                <h3>Productos comprados</h3>

                <table border="1"
                       cellpadding="10"
                       cellspacing="0"
                       style="border-collapse:collapse;">

                    <tr>
                        <th>Producto</th>
                        <th>Cantidad</th>
                        <th>Subtotal</th>
                    </tr>

                    {productos_html_productor}

                </table>

                <br>

                <h3>
                    Total:
                    {precio_colombiano(total)}
                </h3>
                """

                try:

                    send_mail(

                        subject="Nuevo pedido recibido - AgroTolima",

                        message="Tienes un nuevo pedido.",

                        from_email=settings.DEFAULT_FROM_EMAIL,

                        recipient_list=[productor.correo],

                        html_message=html_productor,

                        fail_silently=False

                    )

                    productores_notificados.add(
                        productor.correo
                    )

                except Exception as e:

                    print(
                        "ERROR EMAIL PRODUCTOR:",
                        e
                    )

            # =========================
            # LIMPIAR CARRITO
            # =========================

            request.session["carrito"] = {}

            request.session.modified = True

            messages.success(
                request,
                "Pedido realizado correctamente. El productor confirmara tu pedido pronto."
            )

            return render(
                request,
                "carrito/compra_exitosa.html",
                {
                    "pedido": pedido
                }
            )

        else:
            messages.warning(
                request,
                "Completa todos los campos obligatorios."
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
