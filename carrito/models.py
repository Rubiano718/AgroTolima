from django.db import models
from tienda.models import Producto
from django.contrib.auth.models import User

class CartItem(models.Model):
    session_key = models.CharField(max_length=150)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad}"
    
class Pedido(models.Model):

    ESTADOS = [
        ("recibido", "Pedido recibido"),
        ("confirmado", "Confirmado"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    nombre = models.CharField(
        max_length=120
    )

    correo = models.EmailField()

    telefono = models.CharField(
        max_length=30
    )

    departamento = models.CharField(
        max_length=120
    )

    municipio = models.CharField(
        max_length=120
    )

    direccion = models.CharField(
        max_length=255
    )

    informacion_adicional = models.TextField(
        blank=True,
        null=True
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="recibido"
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Pedido #{self.id}"

class PedidoItem(models.Model):

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="items"
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    cantidad = models.PositiveIntegerField()

    precio = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"