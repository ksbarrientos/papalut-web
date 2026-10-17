from urllib.parse import quote

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
    en_promocion = models.BooleanField(
        default=False, verbose_name="¿En promoción / liquidación?"
    )
    precio_oferta = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        verbose_name="Precio de oferta",
    )

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def _whatsapp_url(self, mensaje):
        return ConfiguracionSitio.get_solo().whatsapp_url(mensaje)

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


class ConfiguracionSitio(models.Model):
    """Configuración global editable desde el admin. Fila única (pk=1)."""

    nombre_tienda = models.CharField(max_length=100, default="Papalut")
    numero_whatsapp = models.CharField(
        max_length=20,
        default="50300000000",
        help_text="Número con código de país sin espacios ni +",
    )
    mensaje_whatsapp_general = models.CharField(
        max_length=255,
        default="Hola Papalut, me gustaría consultar sobre sus productos.",
        help_text="Mensaje al hacer clic en el botón de contacto del header",
    )
    mostrar_banner_anuncio = models.BooleanField(
        default=False, verbose_name="¿Mostrar barra superior de anuncio?"
    )
    texto_banner_anuncio = models.CharField(
        max_length=200,
        blank=True,
        default="¡Rebajas de temporada! Descubre nuestras piezas en liquidación.",
    )
    enlace_banner_anuncio = models.CharField(
        max_length=100,
        blank=True,
        default="?promociones=1",
        help_text="Enlace al hacer clic en el banner",
    )

    class Meta:
        verbose_name = 'configuración del sitio'
        verbose_name_plural = 'configuración del sitio'

    def __str__(self):
        return self.nombre_tienda

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def whatsapp_url(self, mensaje):
        return f'https://wa.me/{self.numero_whatsapp}?text={quote(mensaje)}'


class RedSocial(models.Model):
    class Plataforma(models.TextChoices):
        INSTAGRAM = 'instagram', 'Instagram'
        TIKTOK = 'tiktok', 'TikTok'
        FACEBOOK = 'facebook', 'Facebook'
        WHATSAPP = 'whatsapp', 'WhatsApp'
        OTRO = 'otro', 'Otro'

    nombre = models.CharField(max_length=50)
    plataforma = models.CharField(max_length=20, choices=Plataforma.choices)
    url = models.URLField(help_text="Enlace completo a tu perfil")
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'red social'
        verbose_name_plural = 'redes sociales'

    def __str__(self):
        return f'{self.nombre} ({self.get_plataforma_display()})'
