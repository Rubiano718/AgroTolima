from django import forms
from django.core.validators import EmailValidator, RegexValidator


class FormularioContacto(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo",
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-zÀ-ÖØ-öø-ÿÁÉÍÓÚáéíóúÜüÑñ' -]+$",
                message="Escribe solo letras, espacios, guiones o apostrofes.",
            )
        ],
        widget=forms.TextInput(attrs={
            "placeholder": "Ejemplo: Ana Martinez",
            "autocomplete": "name",
        }),
    )

    email = forms.EmailField(
        label="Correo electronico",
        required=True,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            "placeholder": "correo@ejemplo.com",
            "autocomplete": "email",
        }),
    )

    contenido = forms.CharField(
        label="Mensaje",
        required=True,
        widget=forms.Textarea(attrs={
            "placeholder": "Cuéntanos si necesitas ayuda con un pedido, registro, publicación de productos o una recomendación para mejorar la plataforma.",
            "rows": 7,
        }),
    )
