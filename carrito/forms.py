from django import forms

from tienda.models import normalizar_telefono


class CheckoutForm(forms.Form):

    nombre = forms.CharField(
        max_length=120,
        error_messages={
            "required": "Completa tu nombre completo."
        },
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Nombre completo"
        })
    )

    correo = forms.EmailField(
        error_messages={
            "required": "Completa tu correo electronico.",
            "invalid": "Ingresa un correo electronico valido."
        },
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Correo electronico"
        })
    )

    telefono = forms.CharField(
        max_length=30,
        error_messages={
            "required": "Completa tu telefono."
        },
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Telefono"
        })
    )

    ciudad = forms.CharField(
        max_length=100,
        error_messages={
            "required": "Completa la ciudad de entrega."
        },
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ciudad"
        })
    )

    direccion = forms.CharField(
        max_length=255,
        error_messages={
            "required": "Completa la direccion de entrega."
        },
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Direccion de entrega"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        obligatorios = [
            "nombre",
            "correo",
            "telefono",
            "ciudad",
            "direccion",
        ]

        if any(not cleaned_data.get(campo) for campo in obligatorios):
            raise forms.ValidationError(
                "Completa todos los campos obligatorios."
            )

        return cleaned_data

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono", "").strip()

        if len(normalizar_telefono(telefono)) < 7:
            raise forms.ValidationError(
                "Ingresa un numero de telefono valido."
            )

        return telefono
