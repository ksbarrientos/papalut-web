"""Datos iniciales de Papalut. Idempotente: reejecutable sin duplicar registros."""

import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalogo.models import (  # noqa: E402
    Categoria,
    ConfiguracionSitio,
    FichaPlanta,
    Producto,
    RedSocial,
)

CATEGORIAS = [
    {
        'slug': 'velas',
        'nombre': 'Velas Artesanales',
        'tipo': Categoria.Tipo.VELAS,
        'descripcion': 'Velas de cera vegetal vertidas a mano, pensadas para '
                       'transformar el ambiente con aromas cálidos y envolventes.',
    },
    {
        'slug': 'chocolates',
        'nombre': 'Chocolates Artesanales',
        'tipo': Categoria.Tipo.CHOCOLATES,
        'descripcion': 'Chocolates elaborados en pequeños lotes con cacao de '
                       'origen y combinaciones de sabores cuidadosamente elegidas.',
    },
    {
        'slug': 'plantas',
        'nombre': 'Cactus y Suculentas',
        'tipo': Categoria.Tipo.PLANTAS,
        'descripcion': 'Plantas resistentes y de bajo mantenimiento que aportan '
                       'verde y calma a cualquier rincón.',
    },
    {
        'slug': 'macetas',
        'nombre': 'Macetas de Cemento',
        'tipo': Categoria.Tipo.MACETAS,
        'descripcion': 'Macetas de cemento de acabado mate y líneas limpias, '
                       'moldeadas y pulidas una a una.',
    },
    {
        'slug': 'jabones',
        'nombre': 'Jabones Naturales',
        'tipo': Categoria.Tipo.JABONES,
        'descripcion': 'Jabones de saponificación en frío con ingredientes '
                       'naturales, suaves con la piel y el entorno.',
    },
]

PRODUCTOS = [
    {
        'slug': 'vela-lavanda-manzanilla',
        'categoria': 'velas',
        'nombre': 'Vela Lavanda & Manzanilla',
        'descripcion': 'Vela de cera de soya con mecha de algodón que libera un '
                       'aroma floral y herbal, ideal para rituales de descanso.',
        'notas_olfativas': 'Lavanda, manzanilla y un fondo suave de almizcle blanco.',
        'dimensiones': '8 cm de alto x 7 cm de diámetro',
        'destacado': True,
    },
    {
        'slug': 'vela-vainilla-ambar',
        'categoria': 'velas',
        'nombre': 'Vela Vainilla & Ámbar',
        'descripcion': 'Aroma cálido y dulce que envuelve el espacio, perfecto '
                       'para las tardes en casa.',
        'notas_olfativas': 'Vainilla de Madagascar, ámbar y madera de sándalo.',
        'dimensiones': '10 cm de alto x 8 cm de diámetro',
        'destacado': False,
    },
    {
        'slug': 'tableta-chocolate-70',
        'categoria': 'chocolates',
        'nombre': 'Tableta Chocolate Semi-amargo 70%',
        'descripcion': 'Tableta de origen con cacao al 70%, textura firme y '
                       'final largo en boca.',
        'notas_olfativas': 'Cacao intenso con matices de frutos rojos y café.',
        'dimensiones': '90 g',
        'destacado': True,
        'precio_unitario': '6.00',
        'precio_docena': '60.00',
        'precio_mayoreo': '4.50',
    },
    {
        'slug': 'bombones-cacao-naranja',
        'categoria': 'chocolates',
        'nombre': 'Bombones Rellenos de Cacao & Naranja',
        'descripcion': 'Caja de bombones con ganache de chocolate amargo y un '
                       'toque cítrico de naranja.',
        'notas_olfativas': 'Chocolate amargo y cáscara de naranja.',
        'dimensiones': '12 piezas, caja de 12 x 12 cm',
        'destacado': False,
        'precio_unitario': '12.00',
        'precio_docena': '120.00',
        'precio_mayoreo': '9.00',
    },
    {
        'slug': 'suculenta-echeveria-elegans',
        'categoria': 'plantas',
        'nombre': 'Suculenta Echeveria Elegans',
        'descripcion': 'Roseta compacta de hojas carnosas con un delicado tono '
                       'azulado, fácil de cuidar en interiores luminosos.',
        'notas_olfativas': 'Aroma verde fresco y terroso.',
        'dimensiones': 'Maceta de 6 cm de diámetro',
        'destacado': True,
    },
    {
        'slug': 'cactus-san-pedro-joven',
        'categoria': 'plantas',
        'nombre': 'Cactus San Pedro Joven',
        'descripcion': 'Cactus columnar de crecimiento lento que aporta carácter '
                       'y arquitectura a cualquier espacio.',
        'notas_olfativas': 'Aroma vegetal tenue y limpio.',
        'dimensiones': '10 cm de alto x 6 cm de diámetro',
        'destacado': False,
    },
    {
        'slug': 'maceta-cemento-cilindrica-nordica',
        'categoria': 'macetas',
        'nombre': 'Maceta Cemento Cilíndrica Nórdica',
        'descripcion': 'Maceta de cemento de acabado gris mate y forma cilíndrica '
                       'minimalista, con plato incluido.',
        'notas_olfativas': '',
        'dimensiones': '12 cm de alto x 12 cm de diámetro',
        'destacado': True,
    },
    {
        'slug': 'maceta-cemento-geometrica-terracota',
        'categoria': 'macetas',
        'nombre': 'Maceta Cemento Geométrica Terracota',
        'descripcion': 'Diseño facetado con pigmento terracota que resalta la '
                       'textura natural del cemento.',
        'notas_olfativas': '',
        'dimensiones': '10 cm de alto x 10 cm de diámetro',
        'destacado': False,
    },
    {
        'slug': 'jabon-avena-miel',
        'categoria': 'jabones',
        'nombre': 'Jabón Avena y Miel',
        'descripcion': 'Jabón de saponificación en frío con avena molida y miel '
                       'de abeja, exfoliante suave y humectante.',
        'notas_olfativas': 'Miel, avena tostada y un fondo de leche y almendra.',
        'dimensiones': '100 g',
        'destacado': True,
    },
    {
        'slug': 'jabon-carbon-activado-menta',
        'categoria': 'jabones',
        'nombre': 'Jabón Carbón Activado & Menta',
        'descripcion': 'Jabón purificante con carbón activado y aceite esencial '
                       'de menta, ideal para pieles mixtas.',
        'notas_olfativas': 'Menta fresca, eucalipto y carbón mineral.',
        'dimensiones': '100 g',
        'destacado': False,
    },
]


FICHAS = [
    {
        'producto': 'suculenta-echeveria-elegans',
        'nombre_cientifico': 'Echeveria elegans',
        'familia': 'Crassulaceae',
        'origen': 'México central',
        'luz': 'Interiores muy luminosos o semisombra con sol suave de la mañana.',
        'riego': 'Riego profundo y espaciado: deja secar por completo el sustrato '
                 'entre riegos. Reduce a una vez al mes en invierno.',
        'temperatura': 'Ideal entre 15 y 25 °C; protege de heladas (< 5 °C).',
        'suelo_sustrato': 'Sustrato para cactus y suculentas con excelente drenaje.',
        'abonado': 'Abono diluido para suculentas una vez al mes en primavera y verano.',
        'propagacion': 'Por separación de retoños o por hojas: deja cicatrizar la '
                       'herida 2 días antes de apoyarla sobre sustrato seco.',
        'plagas': 'Cochinilla algodonosa y pulgones en brotes tiernos.',
        'advertencia_toxicidad': '',
        'notas_adicionales': 'Produce pequeñas flores rosadas en espiga durante la '
                             'primavera. Retira hojas secas de la base para evitar hongos.',
    },
    {
        'producto': 'cactus-san-pedro-joven',
        'nombre_cientifico': 'Echinopsis pachanoi (sin. Trichocereus pachanoi)',
        'familia': 'Cactaceae',
        'origen': 'Andes de Ecuador y Perú',
        'luz': 'Pleno sol a semisombra; aclimatar poco a poco al sol directo.',
        'riego': 'Moderado en primavera y verano, dejando secar por completo el '
                 'sustrato entre riegos. Casi nulo en invierno.',
        'temperatura': 'Tolera el calor intenso; proteger de heladas (< 5 °C).',
        'suelo_sustrato': 'Sustrato mineral para cactus con drenaje excelente.',
        'abonado': 'Abono para cactus a media dosis una vez al mes en verano.',
        'propagacion': 'Por esquejes de tallo: cortar, dejar cicatrizar de 1 a 2 '
                       'semanas y plantar en sustrato seco.',
        'plagas': 'Cochinilla algodonosa y araña roja en ambientes secos.',
        'advertencia_toxicidad': 'Contiene alcaloides: manipular con guantes y '
                                 'mantener fuera del alcance de niños y mascotas.',
        'notas_adicionales': 'Crecimiento columnar; en plantas maduras florece de '
                             'noche con grandes flores blancas.',
    },
]


def seed():
    categorias = {}
    for data in CATEGORIAS:
        categoria, _ = Categoria.objects.update_or_create(
            slug=data['slug'],
            defaults={
                'nombre': data['nombre'],
                'tipo': data['tipo'],
                'descripcion': data['descripcion'],
            },
        )
        categorias[data['slug']] = categoria

    for data in PRODUCTOS:
        defaults = {
            'categoria': categorias[data['categoria']],
            'nombre': data['nombre'],
            'descripcion': data['descripcion'],
            'notas_olfativas': data['notas_olfativas'],
            'dimensiones': data['dimensiones'],
            'destacado': data['destacado'],
            'activo': True,
        }
        # Solo se sobrescriben los precios declarados; el resto se respeta.
        for campo in ('precio_unitario', 'precio_docena', 'precio_mayoreo'):
            if campo in data:
                defaults[campo] = data[campo]

        Producto.objects.update_or_create(slug=data['slug'], defaults=defaults)

    for data in FICHAS:
        producto = Producto.objects.get(slug=data['producto'])
        defaults = {campo: valor for campo, valor in data.items() if campo != 'producto'}
        FichaPlanta.objects.update_or_create(producto=producto, defaults=defaults)

    print(f'Categorías: {Categoria.objects.count()}')
    print(f'Productos: {Producto.objects.count()}')
    print(f'Fichas botánicas: {FichaPlanta.objects.count()}')

    configuracion = ConfiguracionSitio.get_solo()
    if configuracion.numero_whatsapp in ('', '50300000000'):
        configuracion.numero_whatsapp = '50378538605'
        configuracion.save()
    print(f'Configuración: {configuracion.nombre_tienda} ({configuracion.numero_whatsapp})')

    if not RedSocial.objects.exists():
        RedSocial.objects.bulk_create([
            RedSocial(
                nombre='Instagram',
                plataforma=RedSocial.Plataforma.INSTAGRAM,
                url='https://instagram.com/papalut',
                orden=1,
            ),
            RedSocial(
                nombre='WhatsApp',
                plataforma=RedSocial.Plataforma.WHATSAPP,
                url='https://wa.me/50378538605',
                orden=2,
            ),
        ])
    print(f'Redes sociales: {RedSocial.objects.count()}')


if __name__ == '__main__':
    seed()
