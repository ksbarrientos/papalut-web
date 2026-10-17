from django.contrib import admin

from .models import Categoria, ConfiguracionSitio, ImagenProducto, Producto, RedSocial


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
    inlines = [ImagenProductoInline]


@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identidad', {'fields': ('nombre_tienda',)}),
        ('Contacto', {'fields': ('numero_whatsapp', 'mensaje_whatsapp_general')}),
        ('Banner de anuncio', {
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
