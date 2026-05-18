from django import forms

from tienda.models import normalizar_telefono


DEPARTAMENTOS = [

    ("", "Selecciona un departamento"),

    ("Amazonas", "Amazonas"),
    ("Antioquia", "Antioquia"),
    ("Arauca", "Arauca"),
    ("Atlántico", "Atlántico"),
    ("Bolívar", "Bolívar"),
    ("Boyacá", "Boyacá"),
    ("Caldas", "Caldas"),
    ("Caquetá", "Caquetá"),
    ("Casanare", "Casanare"),
    ("Cauca", "Cauca"),
    ("Cesar", "Cesar"),
    ("Chocó", "Chocó"),
    ("Córdoba", "Córdoba"),
    ("Cundinamarca", "Cundinamarca"),
    ("Guainía", "Guainía"),
    ("Guaviare", "Guaviare"),
    ("Huila", "Huila"),
    ("La Guajira", "La Guajira"),
    ("Magdalena", "Magdalena"),
    ("Meta", "Meta"),
    ("Nariño", "Nariño"),
    ("Norte de Santander", "Norte de Santander"),
    ("Putumayo", "Putumayo"),
    ("Quindío", "Quindío"),
    ("Risaralda", "Risaralda"),
    ("San Andrés", "San Andrés"),
    ("Santander", "Santander"),
    ("Sucre", "Sucre"),
    ("Tolima", "Tolima"),
    ("Valle del Cauca", "Valle del Cauca"),
    ("Vaupés", "Vaupés"),
    ("Vichada", "Vichada"),

]


class CheckoutForm(forms.Form):

    nombre = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Nombre completo"
        })
    )

    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Correo electrónico"
        })
    )

    telefono = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Número de teléfono"
        })
    )

    departamento = forms.ChoiceField(
        choices=DEPARTAMENTOS,
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "departamento-select"
        })
    )

    municipio = forms.CharField(
        max_length=120,
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "municipio-select"
        })
    )

    direccion = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Dirección exacta"
        })
    )

    informacion_adicional = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Apartamento, referencia, horario de entrega u otra información adicional (opcional)"
        })
    )

    def clean_telefono(self):

        telefono = self.cleaned_data.get("telefono", "").strip()

        if len(normalizar_telefono(telefono)) < 7:

            raise forms.ValidationError(
                "Ingresa un número de teléfono válido."
            )

        return telefono