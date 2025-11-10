from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/<int:user_id>/', views.listar_usuario, name='listar_usuario'),
    path('usuarios/crear', views.crear_usuario, name='crear_usuario'),
    path('usuarios/actualizar/<int:user_id>', views.actualizar_usuario, name='actualizar_usuario'),
    path('usuarios/borrar/<int:user_id>', views.borrar_usuario, name='borrar_usuario'),
    path('usuarios/<int:user_id>/asignar', views.asignar_equipo, name='asignar_equipo'),
    path('usuarios/<int:user_id>/equipo', views.listar_equipo, name='listar_equipo'),

    path('cartas/', views.listar_cartas, name='listar_cartas'),
    path('cartas/<int:id>/', views.detalle_carta, name='detalle_carta'),
    path('cartas/crear/', views.crear_carta, name='crear_carta'),
    path('cartas/<int:id>/actualizar/', views.actualizar_carta, name='actualizar_carta'),
    path('cartas/<int:id>/eliminar/', views.eliminar_carta, name='eliminar_carta'),
    path('equipos/<int:equipo_id>/cartas/<int:carta_id>/asignar/',views.asignar_carta_equipo,
    name='asignar_carta_equipo'),

    path('equipos/media/<int:user_id>/', views.calcular_media_equipo, name='calcular_media_equipo')
]
