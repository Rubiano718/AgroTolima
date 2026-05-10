from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0002_alter_categoriaproducto_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productor",
            name="correo",
            field=models.EmailField(
                blank=True,
                help_text="Correo de contacto del productor o negocio.",
                max_length=254,
            ),
        ),
        migrations.AddField(
            model_name="productor",
            name="whatsapp",
            field=models.CharField(
                blank=True,
                help_text="Numero de WhatsApp con indicativo. Ejemplo: +57 3157556596",
                max_length=20,
            ),
        ),
        migrations.AlterModelOptions(
            name="categoriaproducto",
            options={
                "verbose_name": "Categoria producto",
                "verbose_name_plural": "Categorias de productos",
            },
        ),
        migrations.AlterModelOptions(
            name="producto",
            options={
                "verbose_name": "Producto",
                "verbose_name_plural": "Productos",
            },
        ),
        migrations.AlterModelOptions(
            name="productor",
            options={
                "verbose_name": "Productor",
                "verbose_name_plural": "Productores",
            },
        ),
    ]
