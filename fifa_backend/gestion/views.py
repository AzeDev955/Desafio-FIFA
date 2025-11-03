from django.shortcuts import render, get_object_or_404
from models import *
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

from django.shortcuts import render
from models import Usuario
from django.http import JsonResponse

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
    try:
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
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)


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
        "valoracion_general": carta.valoracion_general
    })

# ------------------ CREAR CARTA ------------------
#Los parametros que vienen con "" al final es porque si no se inserta nada (no es null) se trata como vacio
@csrf_exempt
def crear_carta(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST'])
    
    try:
        data = json.loads(request.body)
        tipo = data.get("tipo")

        if tipo == "JUG":
            carta = CartaJugador(
                nombre=data["nombre"],
                pais=data.get("pais", ""),
                club=data.get("club", ""),
                liga=data.get("liga", ""),
                posicion=data["posicion"],
                ritmo=data["ritmo"],
                tiro=data["tiro"],
                pase=data["pase"],
                regate=data["regate"],
                defensa=data["defensa"],
                fisico=data["fisico"],
            )
        elif tipo == "POR":
            carta = CartaPortero(
                nombre=data["nombre"],
                pais=data.get("pais", ""),
                club=data.get("club", ""),
                liga=data.get("liga", ""),
                posicion="POR",
                estirada=data["estirada"],
                paradas=data["paradas"],
                saque=data["saque"],
                reflejos=data["reflejos"],
                velocidad=data["velocidad"],
                colocacion=data["colocacion"],
            )
        else:
            return HttpResponseBadRequest("Tipo de carta no válido")

        carta.save()
        return JsonResponse({"message": "Carta creada", "id": carta.id}, status=201)
    
    except KeyError as e:
        return HttpResponseBadRequest(f"Falta campo obligatorio: {e}")
    except ValueError as e:
        return HttpResponseBadRequest(str(e))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("JSON inválido")
    
# ------------------ ACTUALIZAR ------------------
@csrf_exempt
def actualizar_carta(request, id):
    if request.method != "PUT":
        return HttpResponseNotAllowed(['PUT'])

    carta = get_object_or_404(Carta, id=id)
    data = json.loads(request.body)
    carta_especifica = getattr(carta, 'cartajugador', getattr(carta, 'cartaportero', None))
    if not carta_especifica:
        return HttpResponseBadRequest("Carta sin subtipo válido")

    for campo, valor in data.items():
        if hasattr(carta_especifica, campo):
            setattr(carta_especifica, campo, valor)
    try:
        carta_especifica.save()
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    return JsonResponse({"message": "Carta actualizada correctamente"})