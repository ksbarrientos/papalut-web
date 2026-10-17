from urllib.parse import quote

from django.conf import settings
from django.db import models


class Categoria(models.Model):
    class Tipo(models.TextChoices):
        VELAS = 'velas', 'Velas'
        CHOCOLATES = 'chocolates', 'Chocolates'
        PLANTAS = 'plantas', 'Plantas'
        MACETAS = 'macetas', 'Macetas'
        JABONES = 'jabones', 'Jabones'

    nombre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos',
    )
    nombre = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True)
    descripcion = models.TextField(blank=True)
    notas_olfativas = models.CharField(max_length=255, blank=True)
    dimensiones = models.CharField(max_length=100, blank=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    destacado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    precio_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    precio_docena = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    precio_mayoreo = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    mostrar_precio_mayoreo = models.BooleanField(
        default=True, verbose_name="¿Mostrar precio mayorista?"
    )

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def _whatsapp_url(self, mensaje):
        return f'https://wa.me/{settings.WHATSAPP_NUMBER}?text={quote(mensaje)}'

    @property
    def whatsapp_url(self):
        return self._whatsapp_url(f'Hola Papalut, me interesa el producto "{self.nombre}".')

    @property
    def whatsapp_url_detalle(self):
        precios = []
        if self.precio_unitario:
            precios.append('individual')
        if self.precio_docena:
            precios.append('docena')
        if self.precio_mayoreo and self.mostrar_precio_mayoreo:
            precios.append('mayoreo')

        detalle = '/'.join(precios) if precios else 'precios'
        mensaje = f'Hola Papalut, me interesa consultar por {self.nombre} (precios {detalle}).'
        return self._whatsapp_url(mensaje)


class ImagenProducto(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='imagenes_secundarias',
    )
    imagen = models.ImageField(upload_to='productos/galeria/')
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f'Imagen de {self.producto.nombre} (#{self.orden})'
