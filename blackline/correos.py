import json
import logging
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

log = logging.getLogger(__name__)


def _enviar(asunto, plantilla, contexto, destinatario):
    """Envía correos mediante la API de Brevo."""

    try:
        html = render_to_string(plantilla, contexto)

        texto = '\n'.join(
            linea.strip()
            for linea in strip_tags(
                html.replace('</td>', ' </td>')
            ).splitlines()
            if linea.strip()
        )

        copia = (
            [{"email": settings.CORREO_NEGOCIO}]
            if settings.CORREO_NEGOCIO else []
        )

        datos = {
            "sender": {
                "name": "BLACKLINE Barbería",
                "email": settings.CORREO,
            },
            "to": [
                {"email": destinatario}
            ],
            "subject": asunto,
            "htmlContent": html,
            "textContent": texto,
        }

        if copia:
            datos["bcc"] = copia

        solicitud = Request(
            "https://api.brevo.com/v3/smtp/email",
            data=json.dumps(datos).encode("utf-8"),
            headers={
                "accept": "application/json",
                "api-key": settings.BREVO_API_KEY,
                "content-type": "application/json",
            },
            method="POST",
        )

        with urlopen(solicitud, timeout=20) as respuesta:
            respuesta.read()

        return True

    except HTTPError as error:
        detalle = error.read().decode("utf-8", errors="replace")
        log.error("Error de Brevo (%s): %s", error.code, detalle)
        return False

    except Exception:
        log.exception(
            "No se pudo enviar el correo a %s", destinatario
        )
        return False


def enviar_confirmacion_cita(cita):
    return _enviar(
        'Confirmación de tu cita · BLACKLINE',
        'blackline/emails/cita.html',
        {'cita': cita},
        cita.correo
    )


def enviar_confirmacion_pedido(pedido):
    return _enviar(
        f'Confirmación de tu compra #{pedido.pk} · BLACKLINE',
        'blackline/emails/pedido.html',
        {
            'pedido': pedido,
            'items': pedido.items.all()
        },
        pedido.correo
    )


def nota_correo(enviado, correo):
    """Mensaje que se muestra al cliente."""

    if not enviado:
        return 'Quedó guardado, pero no pudimos enviar el correo de confirmación.'

    if not settings.CORREO_REAL:
        return '(Modo de prueba: el correo no está configurado.)'

    return f'Te enviamos la confirmación a {correo}.'
