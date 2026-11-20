from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Servicio(models.Model):
    """Servicio que se muestra en la web pública y se administra desde Django."""

    categoria = models.CharField(max_length=80, verbose_name='categoría')
    nombre = models.CharField(max_length=120, verbose_name='nombre')
    descripcion = models.TextField(verbose_name='descripción')
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='precio')
    imagen_url = models.URLField(max_length=500, verbose_name='URL de imagen')
    texto_alternativo = models.CharField(max_length=160, default='', blank=True, verbose_name='texto alternativo')
    destacado = models.BooleanField(default=False, verbose_name='destacado')
    activo = models.BooleanField(default=True, verbose_name='activo')
    orden = models.PositiveIntegerField(default=0, verbose_name='orden')
    creado = models.DateTimeField(auto_now_add=True, verbose_name='creado')
    actualizado = models.DateTimeField(auto_now=True, verbose_name='actualizado')

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'

    def __str__(self):
        return self.nombre


BARBEROS = [
    ('Diego R.', 'Diego R.'),
    ('Alex M.', 'Alex M.'),
    ('Marco L.', 'Marco L.'),
]

HORAS = [(h, h) for h in (
    '10:00', '11:00', '12:00', '13:00', '14:00',
    '16:00', '17:00', '18:00', '19:00', '20:00',
)]


class Cita(models.Model):
    """Cita agendada por un cliente desde la web."""

    PENDIENTE = 'PENDIENTE'
    CONFIRMADA = 'CONFIRMADA'
    COMPLETADA = 'COMPLETADA'
    CANCELADA = 'CANCELADA'
    ESTADOS = [
        (PENDIENTE, 'Pendiente'),
        (CONFIRMADA, 'Confirmada'),
        (COMPLETADA, 'Completada'),
        (CANCELADA, 'Cancelada'),
    ]

    nombre = models.CharField(max_length=120, verbose_name='nombre del cliente')
    telefono = models.CharField(max_length=30, verbose_name='teléfono')
    correo = models.EmailField(blank=True, default='', verbose_name='correo del cliente')
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, related_name='citas', verbose_name='servicio')
    barbero = models.CharField(max_length=40, choices=BARBEROS, verbose_name='barbero')
    fecha = models.DateField(verbose_name='fecha')
    hora = models.CharField(max_length=5, choices=HORAS, verbose_name='hora')
    estado = models.CharField(max_length=12, choices=ESTADOS, default=PENDIENTE, verbose_name='estado')
    creado = models.DateTimeField(auto_now_add=True, verbose_name='creado')

    class Meta:
        ordering = ['fecha', 'hora']
        verbose_name = 'cita'
        verbose_name_plural = 'citas'
        constraints = [
            # Un barbero no puede tener dos citas activas a la misma fecha y hora.
            models.UniqueConstraint(
                fields=['barbero', 'fecha', 'hora'],
                condition=~Q(estado='CANCELADA'),
                name='cita_unica_por_barbero_fecha_hora',
            ),
        ]

    def __str__(self):
        return f'{self.nombre} · {self.servicio} · {self.fecha} {self.hora}'


class Producto(models.Model):
    """Producto de la tienda; se administra desde Django."""

    CATEGORIAS = [('cabello', 'Cabello'), ('barba', 'Barba'), ('accesorios', 'Accesorios')]

    nombre = models.CharField(max_length=120, verbose_name='nombre')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, verbose_name='categoría')
    descripcion = models.CharField(max_length=200, verbose_name='descripción')
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='precio')
    imagen_url = models.URLField(max_length=500, verbose_name='URL de imagen')
    activo = models.BooleanField(default=True, verbose_name='activo')
    orden = models.PositiveIntegerField(default=0, verbose_name='orden')

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    """Compra hecha desde el carrito."""

    nombre = models.CharField(max_length=120, verbose_name='nombre del cliente')
    correo = models.EmailField(verbose_name='correo')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='total')
    creado = models.DateTimeField(auto_now_add=True, verbose_name='creado')

    class Meta:
        ordering = ['-creado']
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'

    def __str__(self):
        return f'Pedido #{self.pk} · {self.nombre} · ${self.total}'


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=120)  # se guarda el nombre y precio del momento de la compra
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f'{self.nombre} × {self.cantidad}'


class Resena(models.Model):
    """Reseña que deja un cliente en la página. El administrador puede ocultarla o responderla."""

    nombre = models.CharField(max_length=60, verbose_name='nombre')
    servicio = models.ForeignKey(Servicio, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='resenas', verbose_name='servicio')
    calificacion = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='calificación')
    comentario = models.TextField(max_length=600, verbose_name='comentario')
    visible = models.BooleanField(default=True, verbose_name='visible en la página')
    respuesta = models.TextField(blank=True, verbose_name='respuesta de BLACKLINE')
    creada = models.DateTimeField(auto_now_add=True, verbose_name='creada')

    class Meta:
        ordering = ['-creada']
        verbose_name = 'reseña'
        verbose_name_plural = 'reseñas'

    def __str__(self):
        return f'{self.nombre} · {self.calificacion}★'
