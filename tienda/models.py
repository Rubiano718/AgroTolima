from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField


def normalizar_telefono(valor):
    return "".join(caracter for caracter in str(valor or "") if caracter.isdigit())


# =========================
# PRODUCTORES
# =========================

class Productor(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productor"
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

    direccion = models.CharField(
        max_length=180,
        blank=True,
        help_text="Direccion de la finca, local o punto de entrega."
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

    def clean(self):
        super().clean()

        if not self.nombre or not self.nombre.strip():
            raise ValidationError({
                "nombre": "Indica el nombre de tu finca o negocio."
            })

        if not self.municipio or not self.municipio.strip():
            raise ValidationError({
                "municipio": "Indica el municipio donde esta tu negocio."
            })

        telefono_normalizado = normalizar_telefono(self.telefono)

        if len(telefono_normalizado) < 7:
            raise ValidationError({
                "telefono": "Ingresa un numero de telefono valido."
            })

        for productor in Productor.objects.exclude(pk=self.pk):
            if normalizar_telefono(productor.telefono) == telefono_normalizado:
                raise ValidationError({
                    "telefono": "Este numero ya pertenece a otro productor."
                })

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

    UNIDAD_CANASTA = "canasta"
    UNIDAD_BULTO = "bulto"
    UNIDAD_KILO = "kilo"
    UNIDAD_LIBRA = "libra"
    UNIDAD_ARROBA = "arroba"
    UNIDAD_MEDIO_BULTO = "medio_bulto"
    UNIDAD_LITRO = "litro"
    UNIDAD_CANTINA = "cantina"
    UNIDAD_CUBETA = "cubeta"
    UNIDAD_DOCENA = "docena"
    UNIDAD_UNIDAD = "unidad"

    TIPOS_UNIDAD = [
        (UNIDAD_CANASTA, "Canasta"),
        (UNIDAD_BULTO, "Bulto"),
        (UNIDAD_KILO, "Kilo"),
        (UNIDAD_LIBRA, "Libra"),
        (UNIDAD_ARROBA, "Arroba"),
        (UNIDAD_MEDIO_BULTO, "Medio bulto"),
        (UNIDAD_LITRO, "Litro"),
        (UNIDAD_CANTINA, "Cantina"),
        (UNIDAD_CUBETA, "Cubeta"),
        (UNIDAD_DOCENA, "Docena"),
        (UNIDAD_UNIDAD, "Unidad"),
    ]

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
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    tipo_unidad = models.CharField(
        max_length=30,
        choices=TIPOS_UNIDAD,
        default=UNIDAD_UNIDAD
    )

    cantidad_unidad = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=1,
        validators=[MinValueValidator(0.01)],
        help_text="Cantidad incluida en cada unidad de venta. Ej: 1 kilo, 12 unidades, 25 kilos."
    )

    stock = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)]
    )

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

    def clean(self):
        super().clean()

        errores = {}

        if not self.nombre or not self.nombre.strip():
            errores["nombre"] = "Ingresa el nombre del producto."

        if not self.descripcion or not self.descripcion.strip():
            errores["descripcion"] = "Describe el producto para que el comprador lo entienda."

        if self.precio is not None and self.precio < 0:
            errores["precio"] = "El precio no puede ser negativo."

        if self.stock is not None and self.stock < 0:
            errores["stock"] = "El stock no puede ser negativo."

        if self.cantidad_unidad is not None and self.cantidad_unidad <= 0:
            errores["cantidad_unidad"] = "La cantidad por unidad debe ser mayor a cero."

        if errores:
            raise ValidationError(errores)

    @property
    def unidad_venta(self):
        return self.get_tipo_unidad_display()

    @property
    def nombre_con_unidad(self):
        return f"{self.unidad_venta} de {self.nombre}"

    def __str__(self):
        return self.nombre
    
class Resena(models.Model):

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="resenas"
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    comentario = models.TextField()

    calificacion = models.IntegerField()

    creado = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.usuario} - {self.producto}"
    
class Favorito(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "usuario",
            "producto"
        )

    def __str__(self):

        return f"{self.usuario} - {self.producto}"
