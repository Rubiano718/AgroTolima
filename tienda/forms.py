from django import forms
from django.contrib.auth.models import User

from allauth.account.forms import SignupForm
from cloudinary.forms import CloudinaryFileField

from .models import (
    Producto,
    Productor,
    Resena,
    ProductoImagen,
    normalizar_telefono,
)


def validar_imagen(archivo):
    if not archivo:
        return archivo

    content_type = getattr(archivo, "content_type", "")
    formatos_validos = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
    }

    if content_type and content_type not in formatos_validos:
        raise forms.ValidationError(
            "La imagen debe estar en formato JPG, PNG, WEBP o GIF."
        )

    max_size = 5 * 1024 * 1024

    if getattr(archivo, "size", 0) > max_size:
        raise forms.ValidationError(
            "La imagen no puede superar 5 MB."
        )

    return archivo


class CustomSignupForm(SignupForm):

    def clean_email(self):
        email = super().clean_email()

        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Este correo ya esta registrado."
            )

        return email


class ProductorForm(forms.ModelForm):

    class Meta:
        model = Productor
        exclude = ("usuario",)
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre de finca o negocio"
            }),
            "municipio": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Ibague"
            }),
            "telefono": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Numero de telefono"
            }),
            "whatsapp": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+57 3157556596"
            }),
            "correo": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "correo@ejemplo.com"
            }),
            "direccion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Vereda, finca, local o punto de entrega"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Cuenta que produces, donde vendes y que hace especial tu negocio."
            }),
            "imagen": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/png,image/jpeg,image/webp,image/gif"
            }),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono", "").strip()
        digitos = normalizar_telefono(telefono)

        if len(digitos) < 7:
            raise forms.ValidationError(
                "Ingresa un numero de telefono valido."
            )

        for productor in Productor.objects.exclude(pk=self.instance.pk):
            if normalizar_telefono(productor.telefono) == digitos:
                raise forms.ValidationError(
                    "Este numero ya pertenece a otro productor."
                )

        return telefono

    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get("whatsapp", "").strip()

        if whatsapp and len(normalizar_telefono(whatsapp)) < 7:
            raise forms.ValidationError(
                "Ingresa un numero de WhatsApp valido."
            )

        return whatsapp

    def clean_imagen(self):
        return validar_imagen(self.cleaned_data.get("imagen"))


class ProductoForm(forms.ModelForm):

    imagen = CloudinaryFileField(
        options={
            "folder": "productos"
        },
        required=False
    )

    imagenes_extra = forms.FileField(
    required=False,
    widget=forms.ClearableFileInput(attrs={
        "multiple": True,
        "class": "form-control"
    })
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
                "placeholder": "Ej: Cafe especial, limon Tahiti, leche fresca"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Describe calidad, origen, disponibilidad y entrega."
            }),
            "precio": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
                "step": "100",
                "placeholder": "Ej: 35000"
            }),
            "tipo_unidad": forms.Select(attrs={
                "class": "form-select"
            }),
            "cantidad_unidad": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0.01",
                "step": "0.01",
                "placeholder": "Ej: 1"
            }),
            "stock": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0"
            }),
            "disponible": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "").strip()

        if not nombre:
            raise forms.ValidationError(
                "Ingresa el nombre del producto."
            )

        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get("descripcion", "").strip()

        if not descripcion:
            raise forms.ValidationError(
                "Describe el producto para que el comprador lo entienda."
            )

        return descripcion

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")

        if precio is None:
            raise forms.ValidationError(
                "Completa el precio del producto."
            )

        if precio < 0:
            raise forms.ValidationError(
                "El precio no puede ser negativo."
            )

        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")

        if stock is None:
            raise forms.ValidationError(
                "Completa el stock disponible."
            )

        if stock < 0:
            raise forms.ValidationError(
                "El stock no puede ser negativo."
            )

        return stock

    def clean_imagen(self):
        return validar_imagen(self.cleaned_data.get("imagen"))


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
                    (5, "5 - Excelente"),
                    (4, "4 - Muy bueno"),
                    (3, "3 - Bueno"),
                    (2, "2 - Regular"),
                    (1, "1 - Malo"),
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
