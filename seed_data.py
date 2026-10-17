"""Datos iniciales de Papalut. Idempotente: reejecutable sin duplicar registros."""

import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalogo.models import Categoria, Producto  # noqa: E402

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
        Producto.objects.update_or_create(
            slug=data['slug'],
            defaults={
                'categoria': categorias[data['categoria']],
                'nombre': data['nombre'],
                'descripcion': data['descripcion'],
                'notas_olfativas': data['notas_olfativas'],
                'dimensiones': data['dimensiones'],
                'destacado': data['destacado'],
                'activo': True,
            },
        )

    print(f'Categorías: {Categoria.objects.count()}')
    print(f'Productos: {Producto.objects.count()}')


if __name__ == '__main__':
    seed()
