from django.contrib import admin
from django.urls import path
from blackline.views import (
    inicio, servicios, citas, productos, contacto, checkout, resenas,
    registro, iniciar_sesion, cerrar_sesion
)

urlpatterns = [
    path('registro/', registro, name='registro'),
path('login/', iniciar_sesion, name='login'),
path('logout/', cerrar_sesion, name='logout'),
    path('admin/', admin.site.urls),

    path('', inicio, name='inicio'),
    path('servicios/', servicios, name='servicios'),
    path('citas/', citas, name='citas'),
    path('productos/', productos, name='productos'),
    path('contacto/', contacto, name='contacto'),
    path('checkout/', checkout, name='checkout'),
    path('resenas/', resenas, name='resenas'),
]
