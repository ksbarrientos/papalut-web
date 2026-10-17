from django.shortcuts import get_object_or_404, render

from .models import Categoria, Producto


def inicio(request):
    categorias = Categoria.objects.all()
    categoria_slug = request.GET.get('categoria')
    categoria_seleccionada = None

    promociones = request.GET.get('promociones') == '1'
    productos = Producto.objects.filter(activo=True).select_related('categoria')

    if categoria_slug:
        categoria_seleccionada = categorias.filter(slug=categoria_slug).first()
        if categoria_seleccionada:
            productos = productos.filter(categoria=categoria_seleccionada)

    if promociones:
        productos = productos.filter(en_promocion=True)

    context = {
        'categorias': categorias,
        'productos': productos,
        'categoria_seleccionada': categoria_seleccionada,
        'promociones': promociones,
    }
    return render(request, 'catalogo/inicio.html', context)


def calculadoras(request):
    return render(request, 'catalogo/calculadoras.html')


def detalle_producto(request, slug):
    producto = get_object_or_404(
        Producto.objects.select_related('categoria').prefetch_related('imagenes_secundarias'),
        slug=slug,
    )
    return render(request, 'catalogo/detalle_producto.html', {'producto': producto})
