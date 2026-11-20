from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Manda un correo de prueba:  python manage.py probar_correo tucorreo@gmail.com"

    def add_arguments(self, parser):
        parser.add_argument("destino")

    def handle(self, *args, **options):
        if not settings.CORREO_REAL:
            self.stdout.write(self.style.WARNING(
                "Gmail NO está configurado: falta la clave en config/correo_local.py. "
                "El correo solo se mostrará aquí abajo (modo prueba)."))
        try:
            send_mail("Prueba BLACKLINE", "Si lees esto, el correo funciona.", settings.DEFAULT_FROM_EMAIL, [options["destino"]])
            if settings.CORREO_REAL:
                self.stdout.write(self.style.SUCCESS("Correo enviado sin errores. Revisa tu bandeja (y Spam)."))
            else:
                self.stdout.write(self.style.WARNING("Modo prueba: no se envió nada real."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"No se pudo enviar: {e}"))
