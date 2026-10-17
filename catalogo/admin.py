from django.contrib import admin

from .models import Categoria, ImagenProducto, Producto


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
        'nombre', 'categoria', 'precio_unitario',
        'mostrar_precio_mayoreo', 'destacado', 'activo',
    )
    list_editable = ('mostrar_precio_mayoreo', 'destacado', 'activo')
    list_filter = ('categoria', 'destacado', 'activo')
    search_fields = ('nombre', 'notas_olfativas')
    prepopulated_fields = {'slug': ('nombre',)}
    inlines = [ImagenProductoInline]
