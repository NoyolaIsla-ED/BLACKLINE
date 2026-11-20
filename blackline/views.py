import json
import time
from decimal import Decimal

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .correos import enviar_confirmacion_cita, enviar_confirmacion_pedido, nota_correo
from .forms import CitaForm, ResenaForm
from .models import BARBEROS, HORAS, Pedido, PedidoItem, Producto, Resena, Servicio


def inicio(request):
    visibles = Resena.objects.filter(visible=True)
    resumen = visibles.aggregate(promedio=Avg('calificacion'), total=Count('id'))
    return render(request, 'blackline/index.html', {
        'servicios': Servicio.objects.filter(activo=True),
        'resenas_inicio': visibles.filter(calificacion__gte=4)[:3],
        'promedio_resenas': resumen['promedio'] or 0,
        'total_resenas': resumen['total'],
    })

def servicios(request):
    return render(request, 'blackline/servicios.html', {
        'servicios': Servicio.objects.filter(activo=True),
    })


@require_http_methods(['GET', 'POST'])
def citas(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            enviado = enviar_confirmacion_cita(cita)
            return JsonResponse({
                'ok': True,
                'mensaje': (
                    f'✓ ¡Listo, {cita.nombre}! Tu cita de {cita.servicio.nombre} con {cita.barbero} '
                    f'quedó registrada para el {cita.fecha:%d/%m/%Y} a las {cita.hora}. '
                    f'{nota_correo(enviado, cita.correo)}'
                ),
            })
        errores = [e for lista in form.errors.values() for e in lista]
        return JsonResponse({'ok': False, 'errores': errores}, status=400)

    return render(request, 'blackline/citas.html', {
        'servicios': Servicio.objects.filter(activo=True),
        'barberos': [b[0] for b in BARBEROS],
        'horas': [h[0] for h in HORAS],
    })


def productos(request):
    return render(request, 'blackline/productos.html', {
        'productos': Producto.objects.filter(activo=True),
    })


def contacto(request):
    return render(request, 'blackline/contacto.html')


@require_POST
def checkout(request):
    """Recibe el carrito (ids y cantidades), recalcula precios con la base de datos y guarda el pedido."""
    def fallo(*errores):
        return JsonResponse({'ok': False, 'errores': list(errores)}, status=400)

    try:
        datos = json.loads(request.body)
        nombre = str(datos.get('nombre', '')).strip()
        correo = str(datos.get('correo', '')).strip()
        cantidades = {}
        for it in datos.get('items') or []:
            pid, qty = int(it['id']), int(it['qty'])
            if qty < 1 or qty > 20:
                return fallo('Cada producto debe tener entre 1 y 20 piezas.')
            cantidades[pid] = cantidades.get(pid, 0) + qty
    except (ValueError, TypeError, KeyError, AttributeError):
        return fallo('No se pudo leer tu carrito. Recarga la página e intenta de nuevo.')

    if not nombre or len(nombre) > 120:
        return fallo('Escribe tu nombre.')
    try:
        validate_email(correo)
    except ValidationError:
        return fallo('Escribe un correo válido.')
    if not cantidades:
        return fallo('Tu carrito está vacío.')

    productos = {p.id: p for p in Producto.objects.filter(activo=True, id__in=cantidades)}
    if len(productos) != len(cantidades):
        return fallo('Algún producto ya no está disponible. Vacía el carrito y vuelve a intentarlo.')

    with transaction.atomic():
        total = sum((productos[i].precio * q for i, q in cantidades.items()), Decimal('0'))
        pedido = Pedido.objects.create(nombre=nombre, correo=correo, total=total)
        PedidoItem.objects.bulk_create([
            PedidoItem(pedido=pedido, producto=productos[i], nombre=productos[i].nombre,
                       precio=productos[i].precio, cantidad=q)
            for i, q in cantidades.items()
        ])

    enviado = enviar_confirmacion_pedido(pedido)
    return JsonResponse({
        'ok': True,
        'mensaje': f'✓ ¡Gracias, {nombre}! Tu compra #{pedido.pk} por ${total:,.2f} quedó registrada. '
                   f'{nota_correo(enviado, correo)}',
    })


RESENAS_POR_PAGINA = 9
SEGUNDOS_ENTRE_RESENAS = 60


def resenas(request):
    """Muestra las reseñas visibles con sus estadísticas y recibe reseñas nuevas."""
    form = ResenaForm()
    if request.method == 'POST':
        if request.POST.get('web'):  # campo trampa: solo los bots lo llenan
            return redirect('resenas')
        ahora = time.time()
        if ahora - request.session.get('ultima_resena', 0) < SEGUNDOS_ENTRE_RESENAS:
            messages.error(request, 'Espera un momento antes de enviar otra reseña.')
            return redirect('resenas')
        form = ResenaForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['ultima_resena'] = ahora
            messages.success(request, '¡Gracias por tu reseña! Ya aparece en la página.')
            return redirect('resenas')

    visibles = Resena.objects.filter(visible=True).select_related('servicio')
    resumen = visibles.aggregate(promedio=Avg('calificacion'), total=Count('id'))
    total = resumen['total']
    cuentas = {r['calificacion']: r['n'] for r in visibles.values('calificacion').annotate(n=Count('id'))}
    distribucion = [
        {'estrellas': n, 'cantidad': cuentas.get(n, 0),
         'porcentaje': round(cuentas.get(n, 0) * 100 / total) if total else 0}
        for n in (5, 4, 3, 2, 1)
    ]
    pagina = Paginator(visibles, RESENAS_POR_PAGINA).get_page(request.GET.get('page'))
    return render(request, 'blackline/resenas.html', {
        'form': form,
        'servicios': Servicio.objects.filter(activo=True),
        'pagina': pagina,
        'total': total,
        'promedio': resumen['promedio'] or 0,
        'promedio_entero': round(resumen['promedio'] or 0),
        'distribucion': distribucion,
    })
