import csv
from decimal import Decimal, InvalidOperation

from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path

from .forms import ProductoCSVImportForm
from .models import (
    Productor,
    CategoriaProducto,
    Producto
)


@admin.register(Productor)
class ProductorAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "municipio",
        "telefono",
        "whatsapp",
        "correo",
    )

    search_fields = (
        "nombre",
        "municipio",
        "telefono",
        "whatsapp",
        "correo",
    )

    fieldsets = (
        ("Datos del productor", {
            "fields": ("nombre", "municipio", "descripcion", "imagen")
        }),
        ("Canales de contacto", {
            "fields": ("telefono", "whatsapp", "correo"),
            "description": "Estos datos alimentan el directorio y los botones de contacto del marketplace."
        }),
    )


@admin.register(CategoriaProducto)
class CategoriaAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
    )


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    change_list_template = "admin/tienda/producto/change_list.html"

    list_display = (
        "nombre",
        "precio",
        "stock",
        "disponible",
        "productor",
        "categoria"
    )

    list_filter = (
        "categoria",
        "disponible"
    )

    search_fields = (
        "nombre",
        "descripcion",
        "productor__nombre",
        "productor__municipio",
        "categoria__nombre",
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "importar-csv/",
                self.admin_site.admin_view(self.importar_csv),
                name="tienda_producto_importar_csv",
            ),
        ]
        return custom_urls + urls

    def importar_csv(self, request):
        if request.method == "POST":
            form = ProductoCSVImportForm(request.POST, request.FILES)

            if form.is_valid():
                archivo = request.FILES["archivo"]
                lineas = archivo.read().decode("utf-8-sig").splitlines()
                lector = csv.DictReader(lineas)
                creados = 0
                errores = []

                for numero_fila, fila in enumerate(lector, start=2):
                    try:
                        categoria, _ = CategoriaProducto.objects.get_or_create(
                            nombre=fila["categoria"].strip()
                        )
                        productor, _ = Productor.objects.get_or_create(
                            nombre=fila["productor"].strip(),
                            defaults={
                                "municipio": fila.get("municipio_productor", "").strip() or "Tolima",
                                "telefono": fila.get("telefono_productor", "").strip() or "Sin telefono",
                                "whatsapp": fila.get("whatsapp_productor", "").strip(),
                                "correo": fila.get("correo_productor", "").strip(),
                                "descripcion": "Productor regional del Tolima",
                            },
                        )

                        precio = Decimal(str(fila["precio"]).replace(".", "").replace(",", "."))
                        disponible_texto = fila.get("disponible", "si").strip().lower()

                        Producto.objects.create(
                            productor=productor,
                            categoria=categoria,
                            nombre=fila["nombre"].strip(),
                            descripcion=fila.get("descripcion", "").strip(),
                            precio=precio,
                            stock=int(fila.get("stock", 1) or 1),
                            disponible=disponible_texto in ("si", "sí", "true", "1", "disponible"),
                        )
                        creados += 1
                    except (KeyError, InvalidOperation, ValueError) as error:
                        errores.append(f"Fila {numero_fila}: {error}")

                if creados:
                    messages.success(request, f"Se importaron {creados} productos.")

                for error in errores[:8]:
                    messages.warning(request, error)

                if len(errores) > 8:
                    messages.warning(request, f"Hay {len(errores) - 8} errores adicionales.")

                return redirect("..")
        else:
            form = ProductoCSVImportForm()

        return render(
            request,
            "admin/tienda/producto/importar_csv.html",
            {"form": form, "title": "Importar productos por CSV"},
        )
