from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from faker import Faker
import random

#-----------------------------Usuarios--------------------------
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

#Crear un usuario
@csrf_exempt
def crear_usuario(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        usuario = Usuario(nombre=data.get('nombre'), apellido=data.get('apellido'), email=data.get('email'))
        try:
            usuario.save()
            return JsonResponse({
                'exito': True, 'Usuario con id': f'{usuario.id}'
            })

        except Exception as e:
            return JsonResponse({
                'exito': False, 'error': str(e)
            })
    else:
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)

#Actualizar un usuario
@csrf_exempt
def actualizar_usuario(request, user_id):
    if request.method == 'PUT' or request.method == 'PATCH':
        data = json.loads(request.body)
        try:
            usuario = Usuario.objects.get(id=user_id)
            if data.get('nombre'):
                usuario.nombre = data.get('nombre')
            if data.get('apellido'):
                usuario.apellido = data.get('apellido')
            if data.get('email'):
                usuario.email = data.get('email')
            usuario.save()
            return JsonResponse({
                'exito': True, 'Usuario con id': f'{usuario.id} actualizado'
            })
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=404)
    else:
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)

#Borrar usuario
@csrf_exempt
def borrar_usuario(request, user_id):
    if request.method == 'DELETE':
        try:
            usuario = Usuario.objects.get(id=user_id)
            usuario.delete()
            return JsonResponse({
                'exito': True,
                'mensaje': 'Usuario borrado correctamente'
            })
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)
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
    return JsonResponse({"detalle": str(carta)})

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

# ------------------ ELIMINAR ------------------
@csrf_exempt
def eliminar_carta(request, id):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(['DELETE'])
    """
    Se debe poder (CRUD) consultar, guardar, actualizar y borrar cartas,
     siempre que no estén asociadas a ningún equipo. El borrado de las cartas debe ser lógico,
     es decir, debe existir un campo para desactivar esa carta y poder ser activada mediante la actualización."
    """

    carta = get_object_or_404(Carta, id=id)
    carta.delete()
    return JsonResponse({"message": "Carta eliminada"})


#------------------Equipo--------------------
fake = Faker('es_ES')

def asignar_equipo(request,user_id):
    global num_porteros
    if request.method != "POST":
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)
    else:
        usuario = get_object_or_404(User, id=user_id)
        if usuario.equipo is None:
            sufijos = ["CF", "United", "FC", "Athletic", "Racing", "Sporting", "Titans", "Rayo", "Franes"]
            nombre_falso = f"{fake.city()} {random.choice(sufijos)}"
            equipo = Equipo.objects.create(nombre=nombre_falso)
            usuario.equipo = equipo
            usuario.save()

            total_jugadores = 0
            num_porteros = 0
            num_defensas = 0
            num_centrocampistas = 0
            num_delanteros = 0
            while total_jugadores < 23 or total_jugadores > 25:
                num_porteros = random.randint(2,3)
                num_defensas = random.randint(8,10)
                num_centrocampistas = random.randint(6,9)
                num_delanteros = random.randint(5,6)
                total_jugadores = (num_porteros +
                                   num_defensas +
                                   num_centrocampistas +
                                   num_delanteros)

            porteros = list(Carta.objects.filter(posicion='POR'))
            porteros_equipo = random.sample(porteros, num_porteros)

            posiciones_defensa = ['DFC', 'LTI', 'LTD']
            defensas = list(Carta.objects.filter(posicion__in=posiciones_defensa))
            defensas_equipo = random.sample(defensas, num_defensas)

            posiciones_centrocampistas = ['MC', 'MI', 'MD']
            centrocampistas = list(Carta.objects.filter(posicion__in=posiciones_centrocampistas))
            centrocampistas_equipo = random.sample(centrocampistas, num_centrocampistas)

            posiciones_delantero = ['DC', 'MP']
            delanteros = list(Carta.objects.filter(posicion__in=posiciones_delantero))
            delanteros_equipo = random.sample(delanteros, num_delanteros)

            jugadores_equipo = delanteros_equipo + centrocampistas_equipo + defensas_equipo + porteros_equipo
            equipo.cartas.add(*jugadores_equipo)

            return JsonResponse({
                'exito': True,
                'equipo': equipo.nombre,
                'id equipo': equipo.id
                                 })
        else:
            return  JsonResponse({'error': 'Este usuario ya tiene un equipo asignado'}, status=404)
