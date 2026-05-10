from decimal import Decimal, InvalidOperation
from urllib.parse import quote

from django import template

register = template.Library()


@register.filter
def precio_colombiano(valor):
    try:
        numero = Decimal(valor)
    except (InvalidOperation, TypeError, ValueError):
        return "$0"

    entero = int(numero)
    return f"${entero:,}".replace(",", ".")


@register.filter
def telefono_whatsapp(valor):
    if not valor:
        return ""

    digitos = "".join(caracter for caracter in str(valor) if caracter.isdigit())

    if len(digitos) == 10:
        return f"57{digitos}"

    return digitos


@register.filter
def whatsapp_producto_url(producto):
    contacto = getattr(producto.productor, "whatsapp", "") or getattr(producto.productor, "telefono", "")
    telefono = telefono_whatsapp(contacto)

    if not telefono:
        return ""

    mensaje = (
        f"Hola, vi el producto {producto.nombre} en AgroTolima. "
        "Quisiera recibir mas informacion sobre precio, disponibilidad y entrega."
    )

    return f"https://wa.me/{telefono}?text={quote(mensaje)}"
