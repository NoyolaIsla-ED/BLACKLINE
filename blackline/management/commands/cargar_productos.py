from django.core.management.base import BaseCommand
from blackline.models import Producto

DATOS = [
    ("Aceite para Barba", "barba", "Hidratación y aroma elegante.", 220, "https://images.unsplash.com/photo-1621607512214-68297480165e?auto=format&fit=crop&w=700&q=85"),
    ("Bálsamo para Barba", "barba", "Control y suavidad durante el día.", 240, "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&w=700&q=85"),
    ("Pomada Matte", "cabello", "Fijación fuerte sin brillo.", 280, "https://images.unsplash.com/photo-1599351431202-1e0f0137899a?auto=format&fit=crop&w=700&q=85"),
    ("Pomada Classic", "cabello", "Acabado clásico y flexible.", 260, "https://images.unsplash.com/photo-1556228578-8c89e6adf883?auto=format&fit=crop&w=700&q=85"),
    ("Peine Blackline", "accesorios", "Resistente y práctico para uso diario.", 150, "https://images.unsplash.com/photo-1585751119414-ef2636f8aede?auto=format&fit=crop&w=700&q=85"),
    ("Cepillo para Barba", "accesorios", "Distribuye aceites y mantiene la forma.", 190, "https://images.unsplash.com/photo-1620331311520-246422fd82f9?auto=format&fit=crop&w=700&q=85"),
]


class Command(BaseCommand):
    help = "Carga los 6 productos iniciales (no duplica ni cambia precios de los que ya existen)."

    def handle(self, *args, **options):
        for orden, (nombre, cat, desc, precio, img) in enumerate(DATOS, start=1):
            Producto.objects.get_or_create(
                nombre=nombre,
                defaults={"categoria": cat, "descripcion": desc, "precio": precio, "imagen_url": img, "orden": orden},
            )
        self.stdout.write(self.style.SUCCESS(f"Productos en la base de datos: {Producto.objects.count()}"))
