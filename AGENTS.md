# Directiva de Proyecto: Papalut Web

## Contexto

Catálogo online y herramientas interactivas de taller para la marca artesanal "Papalut".
Stack: Django 6.1 + SQLite, Django Templates, Tailwind CSS (CDN) y Vanilla JS.

## Entorno y comandos

- El venv es `venv/`. Cada sesión de shell es limpia, así que invoca el intérprete directo en vez de activar:
  `venv\Scripts\python.exe manage.py <cmd>`
- Servidor de desarrollo: `venv\Scripts\python.exe manage.py runserver`
- Migraciones: `... makemigrations` → `... migrate` (SQLite en `db.sqlite3`, ignorado).
- Admin: `... createsuperuser` y entra en `/admin/`.
- Datos de ejemplo: `venv\Scripts\python.exe seed_data.py` (idempotente; recrea categorías y productos por `slug`).
- Dependencias: `venv\Scripts\python.exe -m pip install <pkg>` y luego refresca `requirements.txt` con `pip freeze`.

## Estructura

- `config/` — paquete del proyecto (settings, urls, wsgi/asgi).
- `catalogo/` — app principal: modelos `Categoria`, `Producto` e `ImagenProducto`; `views.py`, `admin.py` (con inline de galería).
- `templates/base.html` — layout con Tailwind CDN, navbar y footer; bloques `title`, `content`, `scripts`.
- `templates/catalogo/` — `inicio.html` (catálogo), `detalle_producto.html` y `calculadoras.html`.
- `static/` — estáticos globales (`STATICFILES_DIRS`).
- `media/` — subidas de usuario (`MEDIA_ROOT`), ignorado en git.

## Rutas y datos

- `/` → `inicio`: lista productos `activo=True`; filtra por `?categoria=<slug>` (slug inválido = sin filtro).
- `/producto/<slug>/` → `detalle_producto`: `get_object_or_404` + `prefetch_related('imagenes_secundarias')`; galería por JS cliente.
- `/herramientas/` → `calculadoras`: cálculos 100% en JS cliente, sin recargar.
- `catalogo/context_processors.papalut` expone `whatsapp_number` a todas las plantillas (registrado en `settings.TEMPLATES`); el navbar lo usa.

## Quirks a recordar

- Django 6.1: `TEMPLATES['DIRS']` es lista; el email usa `MAILERS` (ya no `EMAIL_BACKEND`).
- `WHATSAPP_NUMBER` vive en `config/settings.py`, sobrescribible por variable de entorno. Es un placeholder: reemplázalo por el número real (formato internacional sin `+`).
- `Producto`: helper `_whatsapp_url(mensaje)`; `whatsapp_url` (tarjeta) y `whatsapp_url_detalle` (precios presentes, omite mayoreo si el flag está off).
- `mostrar_precio_mayoreo` controla la card mayorista del detalle, el bloque de precios y la mención en `whatsapp_url_detalle`.
- Logo del navbar: se resuelve solo `static/images/logo.<ext>` (png/svg/webp/jpg/jpeg) vía `catalogo.context_processors.papalut` → `site_logo`; sin archivo solo se muestra el wordmark.
- `templates/` y `static/` usan `.gitkeep` para versionarse vacías.

## Identidad Visual

- Fondo cálido: #F7F1E7
- Terracota: #C97961
- Verde salvia: #8A9A82
- Café tierra (textos principales): #5A4035
- Acento mostaza: #C5A46D
- Lema: "Aromas que transforman espacios".
- Estilo: Artesanal, limpio, tipografías serif para encabezados y sans para interfaz.

## Reglas Técnicas

- Mantén arquitectura limpia y estándar en Django.
- Las calculadoras funcionan del lado del cliente en JS sin recargar la página.
- El catálogo redirige consultas de productos directo a enlaces de WhatsApp.

## Idioma y Comunicación

- Responde y comunícate SIEMPRE en español en todas las interacciones, explicaciones y preguntas.
