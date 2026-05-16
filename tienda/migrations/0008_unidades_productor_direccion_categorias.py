from django.core.validators import MinValueValidator
from django.db import migrations, models


def crear_categorias(apps, schema_editor):
    CategoriaProducto = apps.get_model("tienda", "CategoriaProducto")

    categorias = [
        "Café",
        "Arroz",
        "Cacao",
        "Frutas y verduras",
        "Plátano",
        "Artesanías",
        "Leche y lácteos",
        "Carne",
        "Huevos",
        "Pescados",
    ]

    existentes = {
        categoria.nombre.strip().lower(): categoria
        for categoria in CategoriaProducto.objects.all()
    }

    equivalencias = {
        "cafe": "Café",
        "café": "Café",
        "platano": "Plátano",
        "plátano": "Plátano",
        "artesanias": "Artesanías",
        "artesanías": "Artesanías",
        "leche y lácteos": "Leche y lácteos",
        "leche y lacteos": "Leche y lácteos",
    }

    for categoria in categorias:
        clave = categoria.lower()
        if clave in existentes:
            continue

        alias_existente = next(
            (
                existente
                for existente, canonico in equivalencias.items()
                if canonico == categoria and existente in existentes
            ),
            None
        )

        if alias_existente:
            existente = existentes[alias_existente]
            existente.nombre = categoria
            existente.save(update_fields=["nombre"])
            existentes[clave] = existente
        else:
            existentes[clave] = CategoriaProducto.objects.create(
                nombre=categoria
            )


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0007_favorito"),
    ]

    operations = [
        migrations.AddField(
            model_name="productor",
            name="direccion",
            field=models.CharField(
                blank=True,
                help_text="Direccion de la finca, local o punto de entrega.",
                max_length=180,
            ),
        ),
        migrations.AddField(
            model_name="producto",
            name="cantidad_unidad",
            field=models.DecimalField(
                decimal_places=2,
                default=1,
                help_text="Cantidad incluida en cada unidad de venta. Ej: 1 kilo, 12 unidades, 25 kilos.",
                max_digits=8,
                validators=[MinValueValidator(0.01)],
            ),
        ),
        migrations.AddField(
            model_name="producto",
            name="tipo_unidad",
            field=models.CharField(
                choices=[
                    ("canasta", "Canasta"),
                    ("bulto", "Bulto"),
                    ("kilo", "Kilo"),
                    ("libra", "Libra"),
                    ("arroba", "Arroba"),
                    ("medio_bulto", "Medio bulto"),
                    ("litro", "Litro"),
                    ("cantina", "Cantina"),
                    ("cubeta", "Cubeta"),
                    ("docena", "Docena"),
                    ("unidad", "Unidad"),
                ],
                default="unidad",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="producto",
            name="precio",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=10,
                validators=[MinValueValidator(0)],
            ),
        ),
        migrations.AlterField(
            model_name="producto",
            name="stock",
            field=models.IntegerField(
                default=1,
                validators=[MinValueValidator(0)],
            ),
        ),
        migrations.RunPython(
            crear_categorias,
            migrations.RunPython.noop,
        ),
    ]
