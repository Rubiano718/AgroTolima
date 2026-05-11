from django import forms

from cloudinary.forms import CloudinaryFileField

from .models import Producto, Productor


# =====================================================
# FORM PRODUCTOR
# =====================================================

class ProductorForm(forms.ModelForm):

    imagen = CloudinaryFileField(
        options={
            'folder': "productores"
        },
        required=False
    )

    class Meta:

        model = Productor

        exclude = ["usuario", "created"]

        widgets = {

            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ejemplo: Café El Paraíso"
            }),

            "municipio": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ejemplo: Ibagué"
            }),

            "telefono": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Número de contacto"
            }),

            "whatsapp": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+57 3001234567"
            }),

            "correo": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "correo@ejemplo.com"
            }),

            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Describe tu negocio o productos..."
            }),

        }


# =====================================================
# FORM PRODUCTOS
# =====================================================

class ProductoForm(forms.ModelForm):

    imagen = CloudinaryFileField(
        options={
            'folder': "productos"
        },
        required=False
    )

    class Meta:

        model = Producto

        exclude = ["productor", "created"]

        widgets = {

            "nombre": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),

            "precio": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "stock": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "categoria": forms.Select(attrs={
                "class": "form-select"
            }),

            "disponible": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }
        # =====================================================
# IMPORTAR CSV
# =====================================================

class ProductoCSVImportForm(forms.Form):

    archivo = forms.FileField(
        label="Archivo CSV"
    )