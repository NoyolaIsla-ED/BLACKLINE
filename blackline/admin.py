from django.contrib import admin

from .models import Cita, Pedido, PedidoItem, Producto, Resena, Servicio


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'activo', 'destacado', 'orden', 'actualizado')
    list_editable = ('activo', 'destacado', 'orden')
    list_filter = ('activo', 'destacado', 'categoria')
    search_fields = ('nombre', 'categoria', 'descripcion')
    ordering = ('orden', 'nombre')
    fieldsets = (
        ('Información del servicio', {
            'fields': ('nombre', 'categoria', 'descripcion', 'precio'),
        }),
        ('Imagen', {
            'fields': ('imagen_url', 'texto_alternativo'),
            'description': 'Usa una URL completa de imagen, por ejemplo https://...'
        }),
        ('Publicación', {
            'fields': ('activo', 'destacado', 'orden'),
        }),
    )


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora', 'nombre', 'telefono', 'correo', 'servicio', 'barbero', 'estado', 'creado')
    list_editable = ('estado',)
    list_filter = ('estado', 'barbero', 'fecha', 'servicio')
    search_fields = ('nombre', 'telefono', 'correo')
    date_hierarchy = 'fecha'
    ordering = ('fecha', 'hora')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'activo', 'orden')
    list_editable = ('precio', 'activo', 'orden')
    list_filter = ('activo', 'categoria')
    search_fields = ('nombre', 'descripcion')


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0
    can_delete = False
    readonly_fields = ('producto', 'nombre', 'precio', 'cantidad')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'total', 'creado')
    search_fields = ('nombre', 'correo')
    readonly_fields = ('creado',)
    inlines = [PedidoItemInline]


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('creada', 'nombre', 'estrellas', 'servicio', 'resumen', 'visible', 'respondida')
    list_editable = ('visible',)
    list_filter = ('visible', 'calificacion', 'servicio', 'creada')
    search_fields = ('nombre', 'comentario')
    readonly_fields = ('creada',)
    actions = ['ocultar', 'mostrar']
    fieldsets = (
        ('Reseña del cliente', {'fields': ('nombre', 'servicio', 'calificacion', 'comentario', 'creada')}),
        ('Moderación', {'fields': ('visible', 'respuesta'),
                        'description': 'Si escribes una respuesta, se muestra debajo de la reseña en la página.'}),
    )

    @admin.display(description='calificación', ordering='calificacion')
    def estrellas(self, obj):
        return '★' * obj.calificacion + '☆' * (5 - obj.calificacion)

    @admin.display(description='comentario')
    def resumen(self, obj):
        return obj.comentario[:60] + ('…' if len(obj.comentario) > 60 else '')

    @admin.display(description='respondida', boolean=True)
    def respondida(self, obj):
        return bool(obj.respuesta)

    @admin.action(description='Ocultar reseñas seleccionadas')
    def ocultar(self, request, queryset):
        self.message_user(request, f'{queryset.update(visible=False)} reseña(s) ocultada(s).')

    @admin.action(description='Mostrar reseñas seleccionadas')
    def mostrar(self, request, queryset):
        self.message_user(request, f'{queryset.update(visible=True)} reseña(s) visible(s).')
