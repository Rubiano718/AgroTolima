from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse

from tienda.models import Productor
from .forms import FormularioContacto


def contacto(request):
    form = FormularioContacto(request.POST or None)
    productores = Productor.objects.annotate(
        total_productos=Count("producto")
    ).order_by("municipio", "nombre")

    if request.method == "POST" and form.is_valid():
        nombre = form.cleaned_data["nombre"]
        correo = form.cleaned_data["email"]
        contenido = form.cleaned_data["contenido"]

        if not settings.EMAIL_DELIVERY_ENABLED:
            messages.warning(
                request,
                (
                    "El formulario esta listo, pero falta configurar SENDGRID_API_KEY "
                    f"para enviar correos reales a {settings.CONTACT_EMAIL}."
                ),
            )
            return redirect(reverse("Contacto"))

        msg = EmailMessage(
            subject="Nuevo mensaje desde AgroTolima",
            body=(
                f"Nombre: {nombre}\n"
                f"Correo: {correo}\n\n"
                f"Mensaje:\n{contenido}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL],
            reply_to=[correo],
        )

        try:
            msg.send(fail_silently=False)
            messages.success(
                request,
                "Tu mensaje fue enviado. Te responderemos lo mas pronto posible.",
            )
        except Exception as error:
            print("Error al enviar:", error)
            messages.warning(
                request,
                "No pudimos enviar el correo. Revisa la configuracion de correo o usa WhatsApp.",
            )

        return redirect(reverse("Contacto"))

    return render(request, "contacto/contacto.html", {
        "formulario": form,
        "productores": productores,
    })
