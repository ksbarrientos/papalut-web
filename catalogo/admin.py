from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html

from .models import (
    Categoria,
    ConfiguracionSitio,
    FichaPlanta,
    ImagenProducto,
    Producto,
    RedSocial,
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nombre',)
    prepopulated_fields = {'slug': ('nombre',)}


class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    fields = ('imagen', 'orden')


class FichaPlantaInline(admin.StackedInline):
    """Ficha botánica editable desde la planta, solo para categoría 'plantas'."""

    model = FichaPlanta
    extra = 0
    max_num = 1
    fields = (
        'nombre_cientifico', 'familia', 'origen',
        'luz', 'riego', 'temperatura', 'suelo_sustrato', 'abonado',
        'propagacion', 'plagas', 'advertencia_toxicidad', 'notas_adicionales',
    )


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'categoria', 'precio_unitario', 'en_promocion',
        'mostrar_precio_mayoreo', 'destacado', 'activo',
    )
    list_editable = ('en_promocion', 'mostrar_precio_mayoreo', 'destacado', 'activo')
    list_filter = ('categoria', 'en_promocion', 'destacado', 'activo')
    search_fields = ('nombre', 'notas_olfativas')
    prepopulated_fields = {'slug': ('nombre',)}
    inlines = [ImagenProductoInline, FichaPlantaInline]

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj)
        if obj is not None and obj.categoria.tipo == Categoria.Tipo.PLANTAS:
            return inlines
        return [inline for inline in inlines if not isinstance(inline, FichaPlantaInline)]


@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identidad', {'fields': ('nombre_tienda', 'url_publica_sitio')}),
        ('Contenido de Portada (Hero)', {
            'fields': (
                'hero_subtitulo_superior',
                'hero_titulo',
                'hero_descripcion',
                'eslogan_marca',
            ),
        }),
        ('Contacto', {'fields': ('numero_whatsapp', 'mensaje_whatsapp_general')}),
        ('Banner de Anuncio / Ofertas', {
            'fields': (
                'mostrar_banner_anuncio',
                'texto_banner_anuncio',
                'enlace_banner_anuncio',
            ),
        }),
    )

    def has_add_permission(self, request):
        return not ConfiguracionSitio.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RedSocial)
class RedSocialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'plataforma', 'activo', 'orden', 'url')
    list_editable = ('activo', 'orden')
    list_filter = ('plataforma', 'activo')


@admin.register(FichaPlanta)
class FichaPlantaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'nombre_cientifico', 'familia')
    list_filter = ('familia',)
    search_fields = ('producto__nombre', 'nombre_cientifico', 'familia')
    readonly_fields = ('qr_preview',)
    fieldsets = (
        ('Planta', {'fields': ('producto', 'nombre_cientifico', 'familia', 'origen')}),
        ('Cuidados', {
            'fields': ('luz', 'riego', 'temperatura', 'suelo_sustrato', 'abonado'),
        }),
        ('Reproducción y salud', {
            'fields': (
                'propagacion',
                'plagas',
                'advertencia_toxicidad',
                'notas_adicionales',
            ),
        }),
        ('Código QR (solo admin)', {'fields': ('qr_preview',)}),
    )

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        # Se guarda el request para construir la URL absoluta del QR.
        self._request = request
        return super().render_change_form(request, context, add, change, form_url, obj)

    def _qr_base(self, request):
        return request.build_absolute_uri('/')

    def get_urls(self):
        custom = [
            path(
                '<path:object_id>/qr/',
                self.admin_site.admin_view(self.qr_download_view),
                name='catalogo_fichaplanta_qr',
            ),
        ]
        return custom + super().get_urls()

    def qr_download_view(self, request, object_id):
        ficha = get_object_or_404(FichaPlanta, pk=object_id)
        if not self.has_view_permission(request, ficha):
            raise PermissionDenied('Sin permiso para ver esta ficha.')
        png = ficha.get_qr_png(base_url=self._qr_base(request))
        response = HttpResponse(png, content_type='image/png')
        response['Content-Disposition'] = (
            f'attachment; filename="ficha-{ficha.producto.slug}-qr.png"'
        )
        return response

    @admin.display(description='Código QR de la ficha')
    def qr_preview(self, obj):
        if obj is None or not obj.pk:
            return 'Guarda la ficha para generar el código QR.'

        base = self._qr_base(getattr(self, '_request', None)) if getattr(self, '_request', None) else None
        data_uri = obj.get_qr_data_uri(base_url=base)
        url = reverse('admin:catalogo_fichaplanta_qr', args=[obj.pk])

        return format_html(
            '<div style="display:flex;gap:20px;align-items:center;flex-wrap:wrap">'
            '<img src="{}" alt="Código QR de la ficha" '
            'style="width:180px;height:180px;border:1px solid #ddd;'
            'border-radius:8px;background:#fff;padding:8px">'
            '<div>'
            '<p style="margin:0 0 10px;color:#666">Escape este código para '
            'las etiquetas colgantes de la planta.</p>'
            '<a class="button" href="{}">Descargar QR en alta resolución (PNG)</a>'
            '</div></div>',
            data_uri,
            url,
        )
