from django.shortcuts import render, get_object_or_404
from models import *
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

from django.shortcuts import render
from models import Usuario
from django.http import JsonResponse

# Create your views here.
#Listar todos los usuarios
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    data = []
    for usuario in usuarios:
        data.append({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'email': usuario.email,
            'equipo': usuario.equipo.nombre
        })
    return JsonResponse(data, safe=False)

#Listar un usuario

def listar_usuario(request, user_id):
    usuario = Usuario.objects.get(id=user_id)
    data = []
    if usuario:
        data.append({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'email': usuario.email,
        })
    return JsonResponse(data, safe=False)


#------------------- Cartas ------------------------
# ------------------ LISTAR TODAS ------------------
def listar_cartas(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(['GET'])
    data = list(Carta.objects.values())
    return JsonResponse(data, safe=False)

# ------------------ VER DETALLE ------------------
def detalle_carta(request, id):
    if request.method != "GET":
        return HttpResponseNotAllowed(['GET'])
    carta = get_object_or_404(Carta, id=id)
    return JsonResponse({
        "id": carta.id,
        "nombre": carta.nombre,
        "tipo": carta.tipo,
        "posicion": carta.posicion,
        "valoracion_general": carta.valoracion_general,
    })