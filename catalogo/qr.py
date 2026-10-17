"""Generación de códigos QR en PNG para las etiquetas de fichas botánicas."""

import base64
from io import BytesIO

import qrcode


def build_qr_png(data, *, box_size=10, border=2, color='#5A4035'):
    """Devuelve los bytes de un PNG con el QR que codifica `data`."""
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill_color=color, back_color='white')

    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()


def build_qr_data_uri(data, *, box_size=10, border=2):
    """Igual que `build_qr_png` pero como data-URI listo para incrustar en HTML."""
    png = build_qr_png(data, box_size=box_size, border=border)
    encoded = base64.b64encode(png).decode('ascii')
    return f'data:image/png;base64,{encoded}'
