from django.db import models
from tienda.models import Producto

class CartItem(models.Model):
    session_key = models.CharField(max_length=150)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad}"

