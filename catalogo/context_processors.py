from django.contrib.staticfiles import finders
from django.db.utils import OperationalError, ProgrammingError

from .models import ConfiguracionSitio, RedSocial

LOGO_EXTENSIONS = ('png', 'svg', 'webp', 'jpg', 'jpeg')


def _logo():
    for extension in LOGO_EXTENSIONS:
        name = f'images/logo.{extension}'
        if finders.find(name):
            return name
    return None


def papalut(request):
    """Expone datos de marca globales a todas las plantillas."""
    try:
        configuracion = ConfiguracionSitio.get_solo()
        redes_sociales = list(RedSocial.objects.filter(activo=True))
    except (OperationalError, ProgrammingError):
        # La BD aún no está migrada: se usan valores por defecto.
        configuracion = ConfiguracionSitio()
        redes_sociales = []

    return {
        'configuracion': configuracion,
        'redes_sociales': redes_sociales,
        'site_logo': _logo(),
    }
