import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blackline', '0001_servicio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, verbose_name='nombre del cliente')),
                ('telefono', models.CharField(max_length=30, verbose_name='teléfono')),
                ('barbero', models.CharField(choices=[('Diego R.', 'Diego R.'), ('Alex M.', 'Alex M.'), ('Marco L.', 'Marco L.')], max_length=40, verbose_name='barbero')),
                ('fecha', models.DateField(verbose_name='fecha')),
                ('hora', models.CharField(choices=[('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'), ('13:00', '13:00'), ('14:00', '14:00'), ('16:00', '16:00'), ('17:00', '17:00'), ('18:00', '18:00'), ('19:00', '19:00'), ('20:00', '20:00')], max_length=5, verbose_name='hora')),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('CONFIRMADA', 'Confirmada'), ('COMPLETADA', 'Completada'), ('CANCELADA', 'Cancelada')], default='PENDIENTE', max_length=12, verbose_name='estado')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='citas', to='blackline.servicio', verbose_name='servicio')),
            ],
            options={
                'verbose_name': 'cita',
                'verbose_name_plural': 'citas',
                'ordering': ['fecha', 'hora'],
            },
        ),
        migrations.AddConstraint(
            model_name='cita',
            constraint=models.UniqueConstraint(condition=models.Q(('estado', 'CANCELADA'), _negated=True), fields=('barbero', 'fecha', 'hora'), name='cita_unica_por_barbero_fecha_hora'),
        ),
    ]
