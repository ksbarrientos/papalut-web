from django.conf import settings
from django.contrib.staticfiles import finders

LOGO_EXTENSIONS = ('png', 'svg', 'webp', 'jpg', 'jpeg')


def _logo():
    for extension in LOGO_EXTENSIONS:
        name = f'images/logo.{extension}'
        if finders.find(name):
            return name
    return None


def papalut(request):
    """Expone datos de marca globales a todas las plantillas."""
    return {
        'whatsapp_number': settings.WHATSAPP_NUMBER,
        'site_logo': _logo(),
    }
