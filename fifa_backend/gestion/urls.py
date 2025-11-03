from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/<int:id>/', views.listar_usuario, name='listar_usuario'),
]
