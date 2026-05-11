from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# =========================
# PRODUCTORES
# =========================

class Productor(models.Model):
    usuario = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    nombre = models.CharField(max_length=120)

    municipio = models.CharField(max_length=100)

    telefono = models.CharField(max_length=20)

    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        help_text="Numero de WhatsApp con indicativo. Ejemplo: +57 3157556596"
    )

    correo = models.EmailField(
        blank=True,
        help_text="Correo de contacto del productor o negocio."
    )

    descripcion = models.TextField()

    imagen = CloudinaryField(
        "imagen",
        folder="productores",
        blank=True,
        null=True
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Productor"
        verbose_name_plural = "Productores"

    def __str__(self):
        return self.nombre


# =========================
# CATEGORÍAS
# =========================

class CategoriaProducto(models.Model):

    nombre = models.CharField(max_length=80)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoria producto"
        verbose_name_plural = "Categorias de productos"

    def __str__(self):
        return self.nombre


# =========================
# PRODUCTOS
# =========================

class Producto(models.Model):

    productor = models.ForeignKey(
        Productor,
        on_delete=models.CASCADE
    )

    categoria = models.ForeignKey(
        CategoriaProducto,
        on_delete=models.CASCADE
    )

    nombre = models.CharField(max_length=120)

    descripcion = models.TextField()

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.IntegerField(default=1)

    disponible = models.BooleanField(default=True)

    imagen = CloudinaryField(
        "imagen",
        folder="productos",
        blank=True,
        null=True
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre
