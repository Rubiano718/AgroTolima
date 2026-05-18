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

        html_message = f"""
        <div style="
            font-family:Arial;
            max-width:700px;
            margin:auto;
            background:#ffffff;
            border-radius:14px;
            overflow:hidden;
            border:1px solid #e5e5e5;
        ">

            <div style="
                background:#198754;
                padding:30px;
                color:white;
                text-align:center;
            ">

                <h1 style="margin:0;">
                    AgroTolima Marketplace
                </h1>

                <p style="margin-top:10px;">
                    Nuevo mensaje desde el formulario de contacto
                </p>

            </div>

            <div style="padding:35px;">

                <h2 style="color:#198754;">
                    Información del usuario
                </h2>

                <p>
                    <strong>Nombre:</strong><br>
                    {nombre}
                </p>

                <p>
                    <strong>Correo electrónico:</strong><br>
                    {correo}
                </p>

                <hr style="margin:25px 0;">

                <h2 style="color:#198754;">
                    Mensaje
                </h2>

                <div style="
                    background:#f8f9fa;
                    padding:20px;
                    border-radius:10px;
                    line-height:1.7;
                ">
                    {contenido}
                </div>

            </div>

        </div>
        """

        msg = EmailMessage(

            subject="Nuevo mensaje desde AgroTolima",

            body=html_message,

            from_email=settings.DEFAULT_FROM_EMAIL,

            to=[settings.CONTACT_EMAIL],

            reply_to=[correo],

        )

        msg.content_subtype = "html"

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

    return render(
        request,
        "contacto/contacto.html",
        {
            "formulario": form,
            "productores": productores,
        }
    )