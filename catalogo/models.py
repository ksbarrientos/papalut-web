from urllib.parse import quote

from django.db import models
from django.urls import reverse

from .qr import build_qr_data_uri, build_qr_png


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
    def esta_en_oferta(self):
        """Oferta real: promoción activa y con precio de oferta definido."""
        return self.en_promocion and self.precio_oferta is not None

    @property
    def tiene_precios(self):
        """True si el producto define al menos un precio."""
        return any((self.precio_unitario, self.precio_docena, self.precio_mayoreo))

    @property
    def whatsapp_url(self):
        return self._whatsapp_url(f'Hola Papalut, me interesa el producto "{self.nombre}".')

    @property
    def whatsapp_url_detalle(self):
        if self.tiene_precios:
            mensaje = (
                f'Hola Papalut, me gustaría consultar disponibilidad para '
                f'ordenar: {self.nombre}.'
            )
            if self.esta_en_oferta:
                mensaje += ' ¡Está en promoción!'
        else:
            mensaje = (
                f'Hola Papalut, me gustaría consultar los precios y '
                f'disponibilidad de: {self.nombre}.'
            )
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


class FichaPlanta(models.Model):
    """Guía de cuidados de una planta, enlazada 1:1 con su producto."""

    producto = models.OneToOneField(
        Producto,
        on_delete=models.CASCADE,
        related_name='ficha_botanica',
        limit_choices_to={'categoria__tipo': 'plantas'},
    )
    nombre_cientifico = models.CharField(
        max_length=150, help_text="Ej: Adenium obesum",
    )
    familia = models.CharField(
        max_length=100, blank=True, help_text="Ej: Apocynaceae",
    )
    origen = models.CharField(
        max_length=150, blank=True,
        help_text="Ej: Este de África, Sur de Arabia",
    )
    luz = models.CharField(
        max_length=200, help_text="Ej: Pleno sol o interiores muy luminosos",
    )
    riego = models.TextField(
        help_text="Frecuencia y pautas de riego según estación",
    )
    temperatura = models.CharField(
        max_length=150, blank=True,
        help_text="Ej: Tolera calor, proteger de < 10°C",
    )
    suelo_sustrato = models.CharField(
        max_length=200, blank=True,
        help_text="Ej: Sustrato arenoso con excelente drenaje",
    )
    abonado = models.CharField(
        max_length=200, blank=True,
        help_text="Ej: 2 a 3 veces en verano con abono para suculentas",
    )
    propagacion = models.TextField(
        blank=True, help_text="Cómo propagar por esquejes o retoños",
    )
    plagas = models.CharField(
        max_length=200, blank=True,
        help_text="Ej: Pulgones, cochinilla algodonosa",
    )
    advertencia_toxicidad = models.CharField(
        max_length=255, blank=True,
        help_text="Ej: Savia irritante, mantener alejado de mascotas",
    )
    notas_adicionales = models.TextField(
        blank=True,
        help_text="Detalles de floración, poda o reposo invernal",
    )

    class Meta:
        verbose_name = 'ficha botánica'
        verbose_name_plural = 'fichas botánicas'

    def __str__(self):
        return f'Ficha de {self.producto.nombre}'

    def get_relative_url(self):
        return reverse('ficha_cuidados', args=[self.producto.slug])

    def get_absolute_url(self, base_url=None):
        # El dominio configurado en la BD tiene prioridad; el host de la
        # petición solo se usa como respaldo (p. ej. en desarrollo).
        configured = ConfiguracionSitio.get_solo().url_publica_sitio
        base = (configured or base_url or '').rstrip('/')
        return f'{base}{self.get_relative_url()}'

    def get_qr_png(self, *, base_url=None, box_size=16, border=4):
        return build_qr_png(self.get_absolute_url(base_url), box_size=box_size, border=border)

    def get_qr_data_uri(self, *, base_url=None, box_size=8, border=2):
        return build_qr_data_uri(self.get_absolute_url(base_url), box_size=box_size, border=border)

    @property
    def whatsapp_url(self):
        mensaje = (
            f'Hola Papalut, tengo una consulta sobre el cuidado de mi '
            f'{self.producto.nombre}.'
        )
        return ConfiguracionSitio.get_solo().whatsapp_url(mensaje)


class ConfiguracionSitio(models.Model):
    """Configuración global editable desde el admin. Fila única (pk=1)."""

    nombre_tienda = models.CharField(max_length=100, default="Papalut")
    url_publica_sitio = models.URLField(
        blank=True,
        verbose_name="URL pública del sitio",
        help_text="Dominio usado en los códigos QR de las fichas (ej. "
                  "https://papalut.com). Si se deja vacío se usa el host actual.",
    )
    hero_subtitulo_superior = models.CharField(
        max_length=100,
        default="HECHO A MANO",
        verbose_name="Texto superior pequeño (Kicker)",
    )
    hero_titulo = models.CharField(
        max_length=150,
        default="Catálogo Papalut",
        verbose_name="Título principal del catálogo",
    )
    hero_descripcion = models.TextField(
        default=(
            "Velas, chocolates, plantas, macetas y jabones creados en pequeños "
            "lotes, con la calma y el detalle de lo artesanal."
        ),
        verbose_name="Párrafo descriptivo principal",
    )
    eslogan_marca = models.CharField(
        max_length=200,
        default="Aromas que transforman espacios.",
        verbose_name="Eslogan de la marca (Hero y Footer)",
    )
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
