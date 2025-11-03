from django.shortcuts import render, get_object_or_404
from models import *
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})
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