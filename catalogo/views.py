from django.shortcuts import get_object_or_404, render

from .models import Categoria, FichaPlanta, Producto


def inicio(request):
    # Solo categorías con al menos un producto activo.
    categorias = Categoria.objects.filter(productos__activo=True).distinct()
    categoria_slug = request.GET.get('categoria')
    categoria_seleccionada = None

    promociones = request.GET.get('promociones') == '1'
    productos = Producto.objects.filter(activo=True).select_related('categoria')

    if categoria_slug:
        # Slug inexistente o categoría sin productos activos: se ignora el filtro.
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


def ficha_cuidados(request, slug):
    ficha = get_object_or_404(
        FichaPlanta.objects.select_related(
            'producto', 'producto__categoria',
        ).prefetch_related('producto__imagenes_secundarias'),
        producto__slug=slug,
        producto__activo=True,
    )

    relacionados = list(
        Producto.objects.filter(activo=True)
        .exclude(id=ficha.producto.id)
        .select_related('categoria')[:4]
    )

    return render(
        request,
        'catalogo/ficha_cuidados.html',
        {'ficha': ficha, 'relacionados': relacionados},
    )


def detalle_producto(request, slug):
    producto = get_object_or_404(
        Producto.objects.select_related('categoria').prefetch_related('imagenes_secundarias'),
        slug=slug,
    )

    relacionados = list(
        Producto.objects.filter(categoria=producto.categoria, activo=True)
        .exclude(id=producto.id)
        .select_related('categoria')[:4]
    )

    faltantes = 4 - len(relacionados)
    if faltantes > 0:
        excluidos = [producto.id] + [p.id for p in relacionados]
        otros = Producto.objects.filter(activo=True).exclude(id__in=excluidos).select_related('categoria')[:faltantes]
        relacionados.extend(otros)

    return render(
        request,
        'catalogo/detalle_producto.html',
        {'producto': producto, 'relacionados': relacionados},
    )
