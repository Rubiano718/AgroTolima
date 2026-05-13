from django import forms

from cloudinary.forms import CloudinaryFileField

from .models import Producto, Productor

from .models import Resena


class ProductorForm(forms.ModelForm):

    class Meta:

        model = Productor

        exclude = ("usuario",)

        widgets = {

            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre del negocio"
            }),

            "municipio": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Ibagué"
            }),

            "telefono": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Número de teléfono"
            }),

            "whatsapp": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+57 3157556596"
            }),

            "correo": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "correo@ejemplo.com"
            }),

            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Describe tu negocio..."
            }),

        }


class ProductoForm(forms.ModelForm):

    imagen = CloudinaryFileField(
        options={
            'folder': "productos"
        },
        required=False
    )

    class Meta:

        model = Producto

        exclude = ("productor",)

        widgets = {

            "categoria": forms.Select(attrs={
                "class": "form-select"
            }),

            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Café Premium"
            }),

            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Describe el producto..."
            }),

            "precio": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: 15000"
            }),

            "stock": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "disponible": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }


class ProductoCSVImportForm(forms.Form):

    archivo = forms.FileField(
        label="Archivo CSV"
    )

class ResenaForm(forms.ModelForm):

    class Meta:

        model = Resena

        fields = [
            "calificacion",
            "comentario"
        ]

        widgets = {

            "calificacion": forms.Select(
                choices=[
                    (5, "⭐⭐⭐⭐⭐ Excelente"),
                    (4, "⭐⭐⭐⭐ Muy bueno"),
                    (3, "⭐⭐⭐ Bueno"),
                    (2, "⭐⭐ Regular"),
                    (1, "⭐ Malo"),
                ],
                attrs={
                    "class": "form-select"
                }
            ),

            "comentario": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Comparte tu experiencia..."
                }
            )
        }