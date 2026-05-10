from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import Producto

class ProductoForm(forms.ModelForm):
    imagen = CloudinaryFileField(
        options={
            'folder': "productos"
        },
        required=False
    )

    class Meta:
        model = Producto
        fields = "__all__"


class ProductoCSVImportForm(forms.Form):
    archivo = forms.FileField(
        label="Archivo CSV",
        help_text=(
            "Columnas: nombre, descripcion, precio, stock, disponible, "
            "categoria, productor, municipio_productor, telefono_productor, "
            "whatsapp_productor, correo_productor"
        )
    )
