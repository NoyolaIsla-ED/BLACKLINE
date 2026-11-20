import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

log = logging.getLogger(__name__)


def _enviar(asunto, plantilla, contexto, destinatario):
    """Manda un correo con diseño HTML (y versión de texto). Devuelve True si salió sin errores."""
    html = render_to_string(plantilla, contexto)
    texto = '\n'.join(l.strip() for l in strip_tags(html.replace('</td>', ' </td>')).splitlines() if l.strip())
    copia = [settings.CORREO_NEGOCIO] if settings.CORREO_NEGOCIO else []
    mensaje = EmailMultiAlternatives(asunto, texto, settings.DEFAULT_FROM_EMAIL, [destinatario], bcc=copia)
    mensaje.attach_alternative(html, 'text/html')
    try:
        mensaje.send()
        return True
    except Exception:
        log.exception('No se pudo enviar el correo a %s', destinatario)
        return False


def enviar_confirmacion_cita(cita):
    return _enviar('Confirmación de tu cita · BLACKLINE', 'blackline/emails/cita.html',
                   {'cita': cita}, cita.correo)


def enviar_confirmacion_pedido(pedido):
    return _enviar(f'Confirmación de tu compra #{pedido.pk} · BLACKLINE', 'blackline/emails/pedido.html',
                   {'pedido': pedido, 'items': pedido.items.all()}, pedido.correo)


def nota_correo(enviado, correo):
    """Frase que se muestra al cliente en la página sobre el correo."""
    if not enviado:
        return 'Quedó guardado, pero no pudimos enviar el correo de confirmación.'
    if not settings.CORREO_REAL:
        return '(Modo prueba: Gmail no está configurado, el correo solo se muestra en la terminal.)'
    return f'Te enviamos la confirmación a {correo}.'
