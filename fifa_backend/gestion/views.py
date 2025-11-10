from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from faker import Faker
import random
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg

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
            'equipo': usuario.equipo.nombre if usuario.equipo else None
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
                'equipo': usuario.equipo.nombre if usuario.equipo else None
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
    data = list(Carta.objects.filter(activa=True).values())
    return JsonResponse(data, safe=False)

# ------------------ VER DETALLE ------------------
def detalle_carta(request, id):
    if request.method != "GET":
        return HttpResponseNotAllowed(['GET'])
    carta = get_object_or_404(Carta, id=id)
    if hasattr(carta, 'cartajugador'):
        carta = carta.cartajugador
    elif hasattr(carta, 'cartaportero'):
        carta = carta.cartaportero

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
        elif hasattr(carta, campo):
            setattr(carta, campo, valor)

    try:
        carta_especifica.save()
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    return JsonResponse({"message": "Carta actualizada correctamente"})

# ------------------ ELIMINAR ------------------
@csrf_exempt
def eliminar_carta(request, id):
    try:
        carta = Carta.objects.get(id=id)
        carta.activa = False
        carta.save()

        return JsonResponse({
            "mensaje": f"Carta '{carta.nombre}' desactivada correctamente.",
            "id": carta.id,
            "activa": carta.activa
        }, status=200)

    except Carta.DoesNotExist:
        return JsonResponse({'error': 'Carta no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


#------------------Equipo--------------------
fake = Faker('es_ES')
@csrf_exempt
def asignar_equipo(request,user_id):
    global num_porteros
    if request.method != "POST":
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)
    else:
        usuario = get_object_or_404(Usuario, id=user_id)
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


def listar_equipo(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if usuario.equipo is None:
        return JsonResponse({'error': 'Este usuario no tiene asignado un equipo'}, status=404)
    else:
        equipo = usuario.equipo
        cartas = equipo.cartas.all().filter(activa=True)
        porteros = equipo.cartas.all().filter(activa=True, posicion='POR')
        defensas = equipo.cartas.all().filter(activa=True, posicion__in=['DC', 'LTI', 'LTD'])
        centrocampistas = equipo.cartas.all().filter(activa=True, posicion__in=['MC', 'MI', 'MD'])
        delanteros = equipo.cartas.all().filter(activa=True, posicion__in=['DC', 'MP'])
        data = []
        for carta in cartas:
            data.append({
                'id': carta.id,
                'nombre': carta.nombre,
                'pais': carta.pais,
                'club': carta.club,
                'liga': carta.liga,
                'posicion': carta.posicion,
                'valoracion': carta.valoracion_general
            })

        return JsonResponse({
            'equipo': equipo.nombre,
            'cantidad' : len(cartas),
            'porteros': len(porteros),
            'defensas': len(defensas),
            'centrocampistas': len(centrocampistas),
            'delanteros': len(delanteros),
            'cartas': data
        })

# ------------------ AÑADIR CARTA A EQUIPO ------------------
@csrf_exempt
def asignar_carta_equipo(request, user_id, carta_id):
    if request.method != "POST":
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)

    # 1) Usuario y equipo
    usuario = get_object_or_404(Usuario, id=user_id)

    if usuario.equipo is None:
        return JsonResponse(
            {'error': 'Este usuario no tiene asignado un equipo'},
            status=404
        )

    equipo = usuario.equipo

    # 2) Carta
    try:
        carta = Carta.objects.get(id=carta_id)
    except Carta.DoesNotExist:
        return JsonResponse({'error': 'Carta no encontrada'}, status=404)

    if not carta.activa:
        return JsonResponse(
            {'error': 'No se puede añadir una carta inactiva al equipo'},
            status=400
        )

    # 3) Ya pertenece al equipo
    if equipo.cartas.filter(id=carta.id).exists():
        return JsonResponse(
            {'error': 'Esta carta ya pertenece a este equipo'},
            status=400
        )

    # 4) Límite total de jugadores (23–25, pero solo miramos el máximo)
    total_actual = equipo.cartas.count()
    if total_actual >= 25:
        return JsonResponse(
            {'error': 'El equipo ya tiene el máximo de 25 jugadores'},
            status=400
        )

    # 5) Límite por posición (mismo criterio que en asignar_equipo)
    posiciones_defensa = ['DFC', 'LTI', 'LTD']
    posiciones_centrocampistas = ['MC', 'MI', 'MD']
    posiciones_delantero = ['DC', 'MP']

    MAX_PORTEROS = 3
    MAX_DEFENSAS = 10
    MAX_CENTROCAMPISTAS = 9
    MAX_DELANTEROS = 6

    porteros_actuales = equipo.cartas.filter(posicion='POR').count()
    defensas_actuales = equipo.cartas.filter(
        posicion__in=posiciones_defensa
    ).count()
    centrocampistas_actuales = equipo.cartas.filter(
        posicion__in=posiciones_centrocampistas
    ).count()
    delanteros_actuales = equipo.cartas.filter(
        posicion__in=posiciones_delantero
    ).count()

    pos = carta.posicion

    if pos == 'POR' and porteros_actuales >= MAX_PORTEROS:
        return JsonResponse(
            {'error': f'No se pueden añadir más de {MAX_PORTEROS} porteros'},
            status=400
        )

    if pos in posiciones_defensa and defensas_actuales >= MAX_DEFENSAS:
        return JsonResponse(
            {'error': f'No se pueden añadir más de {MAX_DEFENSAS} defensas'},
            status=400
        )

    if pos in posiciones_centrocampistas and centrocampistas_actuales >= MAX_CENTROCAMPISTAS:
        return JsonResponse(
            {
                'error': (
                    f'No se pueden añadir más de '
                    f'{MAX_CENTROCAMPISTAS} centrocampistas'
                )
            },
            status=400
        )

    if pos in posiciones_delantero and delanteros_actuales >= MAX_DELANTEROS:
        return JsonResponse(
            {'error': f'No se pueden añadir más de {MAX_DELANTEROS} delanteros'},
            status=400
        )

    # 6) Si pasa todos los filtros, añadimos la carta
    equipo.cartas.add(carta)

    # Recalculamos totales después de añadir
    total_nuevo = equipo.cartas.count()
    porteros_nuevo = equipo.cartas.filter(posicion='POR').count()
    defensas_nuevo = equipo.cartas.filter(
        posicion__in=posiciones_defensa
    ).count()
    centrocampistas_nuevo = equipo.cartas.filter(
        posicion__in=posiciones_centrocampistas
    ).count()
    delanteros_nuevo = equipo.cartas.filter(
        posicion__in=posiciones_delantero
    ).count()

    return JsonResponse({
        'exito': True,
        'mensaje': 'Carta asignada correctamente al equipo',
        'equipo': equipo.nombre,
        'id equipo': equipo.id,
        'id carta': carta.id,
        'total_jugadores': total_nuevo,
        'porteros': porteros_nuevo,
        'defensas': defensas_nuevo,
        'centrocampistas': centrocampistas_nuevo,
        'delanteros': delanteros_nuevo
    }, status=200)

@csrf_exempt
def ejercicio(request, user_id):
    try:
        usuario = Usuario.objects.get(id=user_id)
        
        equipo = usuario.equipo 

        cartas = equipo.cartas.filter(activa=True)

        if not cartas.exists():
                raise CommandError(
                    f"El equipo '{equipo.nombre}' del usuario {usuario} no tiene cartas activas."
                )
        
        media = cartas.aggregate(media=Avg("valoracion_general"))["media"]
        media = int(round(media,0))
        if media >= 0 & media < 19:
            funciona="*"

        if media > 20 & media <39:
            funciona="**"
        
        if media > 40 & media <59:
            funciona="***"
        
        if media > 60 & media <79:
            funciona="****"

        else:
            funciona="*****"

        data = []
        if usuario:
            data.append({
                    'id': usuario.id,
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'email': usuario.email,
                    'equipo': usuario.equipo.nombre if usuario.equipo else None,
                    'media equipo' : funciona
            })

        return JsonResponse(data, safe=False)
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)    