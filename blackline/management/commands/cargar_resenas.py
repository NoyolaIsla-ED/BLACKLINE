from django.core.management.base import BaseCommand
from blackline.models import Resena

DATOS = [
    ("Carlos M.", 5, "Excelente atención y el fade quedó exactamente como lo pedí. El ambiente está increíble."),
    ("Daniel R.", 5, "Desde que conocí Blackline ya no busco otra barbería. Muy profesionales."),
    ("Luis A.", 5, "La experiencia completa vale totalmente la pena. Todo está muy cuidado."),
    ("Jorge S.", 4, "Muy buen corte y buen trato. Solo que tuve que esperar un poco más de lo planeado."),
]


class Command(BaseCommand):
    help = "Carga 4 reseñas de ejemplo (no duplica las que ya existen)."

    def handle(self, *args, **options):
        for nombre, estrellas, texto in DATOS:
            Resena.objects.get_or_create(nombre=nombre, comentario=texto, defaults={"calificacion": estrellas})
        self.stdout.write(self.style.SUCCESS(f"Reseñas en la base de datos: {Resena.objects.count()}"))
