from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from cloudinary.models import CloudinaryField   # ✔ IMPORTANTE

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, validators=[RegexValidator(
        regex=r"^[A-Za-zÁÉÍÓÚáéíóúÜüÑñ' -]+$",
        message="Solo se permiten letras, espacios, guiones y apóstrofes."
    )])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nombre
    

class Post(models.Model):
    titulo = models.CharField(max_length=50)
    contenido = models.TextField(max_length=100)

    # ✔ AHORA USAMOS CLOUDINARY (igual que productos)
    imagen = CloudinaryField('image', blank=True, null=True)

    autor = models.ForeignKey(User, on_delete=models.PROTECT)
    categorias = models.ManyToManyField(Categoria)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.titulo

