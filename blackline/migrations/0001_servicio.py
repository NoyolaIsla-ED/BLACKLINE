from decimal import Decimal

from django.db import migrations, models


SERVICIOS_INICIALES = [
    {'categoria': 'CORTE', 'nombre': 'Fade + Corte', 'descripcion': 'Degradado personalizado, tijera o máquina y acabado profesional.', 'precio': Decimal('250.00'), 'imagen_url': 'https://images.unsplash.com/photo-1622286342621-4bd786c2447c?auto=format&fit=crop&w=900&q=85', 'texto_alternativo': 'Corte fade moderno', 'destacado': False, 'orden': 1},
    {'categoria': 'CORTE + BARBA', 'nombre': 'Corte + Barba', 'descripcion': 'Corte completo más perfilado y definición de barba.', 'precio': Decimal('300.00'), 'imagen_url': 'https://images.unsplash.com/photo-1621605815847-2f7f8f1d3e40?auto=format&fit=crop&w=900&q=85', 'texto_alternativo': 'Corte y barba profesional', 'destacado': False, 'orden': 2},
    {'categoria': 'BARBA', 'nombre': 'Barba Premium', 'descripcion': 'Navaja, toalla caliente, perfilado e hidratación.', 'precio': Decimal('180.00'), 'imagen_url': 'https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=900&q=85', 'texto_alternativo': 'Barbero trabajando una barba', 'destacado': False, 'orden': 3},
    {'categoria': 'EXPERIENCIA COMPLETA', 'nombre': 'Blackline Experience', 'descripcion': 'Corte, barba, toalla caliente y acabado premium.', 'precio': Decimal('350.00'), 'imagen_url': 'https://images.unsplash.com/photo-1512690459411-b9245aed614b?auto=format&fit=crop&w=900&q=85', 'texto_alternativo': 'Interior de barbería premium', 'destacado': True, 'orden': 4},
]


def crear_servicios(apps, schema_editor):
    Servicio = apps.get_model('blackline', 'Servicio')
    for servicio in SERVICIOS_INICIALES:
        Servicio.objects.create(**servicio)


def eliminar_servicios(apps, schema_editor):
    apps.get_model('blackline', 'Servicio').objects.all().delete()


class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=80, verbose_name='categoría')),
                ('nombre', models.CharField(max_length=120, verbose_name='nombre')),
                ('descripcion', models.TextField(verbose_name='descripción')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='precio')),
                ('imagen_url', models.URLField(max_length=500, verbose_name='URL de imagen')),
                ('texto_alternativo', models.CharField(blank=True, default='', max_length=160, verbose_name='texto alternativo')),
                ('destacado', models.BooleanField(default=False, verbose_name='destacado')),
                ('activo', models.BooleanField(default=True, verbose_name='activo')),
                ('orden', models.PositiveIntegerField(default=0, verbose_name='orden')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='actualizado')),
            ],
            options={'verbose_name': 'servicio', 'verbose_name_plural': 'servicios', 'ordering': ['orden', 'id']},
        ),
        migrations.RunPython(crear_servicios, eliminar_servicios),
    ]
