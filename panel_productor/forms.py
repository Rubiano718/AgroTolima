from django import forms

from tienda.models import (
    Productor,
    Producto
)


class RegistroProductorForm(forms.ModelForm):

    class Meta:
        model = Productor

        fields = [
            "nombre",
            "municipio",
            "telefono",
            "whatsapp",
            "correo",
            "descripcion",
            "imagen",
        ]


class ProductoProductorForm(forms.ModelForm):

    class Meta:
        model = Producto

        fields = [
            "categoria",
            "nombre",
            "descripcion",
            "precio",
            "stock",
            "disponible",
            "imagen",
        ]