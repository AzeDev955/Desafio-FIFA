from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/<int:user_id>/', views.listar_usuario, name='listar_usuario'),
    path('usuarios/crear', views.crear_usuario, name='crear_usuario'),

    path('cartas/', views.listar_cartas, name='listar_cartas'),
    path('cartas/<int:id>/', views.detalle_carta, name='detalle_carta'),
    path('cartas/crear/', views.crear_carta, name='crear_carta'),
    path('cartas/<int:id>/actualizar/', views.actualizar_carta, name='actualizar_carta'),
    path('cartas/<int:id>/eliminar/', views.eliminar_carta, name='eliminar_carta')
]
