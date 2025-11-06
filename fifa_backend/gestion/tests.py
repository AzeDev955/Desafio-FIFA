import json
from django.test import TestCase
from .models import *
import faker as fake
import random
# Create your tests here.
fake = fake.Faker('es_ES')

class UsuarioTest(TestCase):
    def test_crear_usuario_modelo(self):
        usuario = Usuario(
            nombre = 'TestNombre',
            apellido = 'TestApellido',
            email = 'TestCorreo@test.com'
        )
        usuario.save()

        usuarioTest = Usuario.objects.get(email='TestCorreo@test.com')

        self.assertEqual(usuario.email,usuarioTest.email)

    def test_listar_usuarios(self):
        usuarioTest = Usuario(
            nombre = 'TestNombre',
            apellido = 'TestApellido',
            email = 'TestCorreo@test.com'
        )
        usuarioTest.save()
        respuesta = self.client.get('/gestion/usuarios/')

        self.assertEqual(respuesta.status_code,200)
        #La b es para pasarlo a bytes, que es lo que puede leer el assertIn
        self.assertIn(b'TestNombre',respuesta.content)

    def test_listar_un_usuario(self):
        usuarioTest = Usuario(
            nombre='TestNombre',
            apellido='TestApellido',
            email='TestCorreo@test.com'
        )
        usuarioTest.save()
        idTest = usuarioTest.id
        respuesta = self.client.get(f'/gestion/usuarios/{idTest}/')

        self.assertEqual(respuesta.status_code, 200)

        self.assertIn(b'TestNombre', respuesta.content)

    def test_crear_usuario_vista(self):
        datosUsuario = {
            'nombre': 'TestNombre',
            'apellido': 'TestApellido',
            'email': 'TestCorreo@test.com'
        }

        respuesta = self.client.post('/gestion/usuarios/crear',data=datosUsuario,content_type='application/json')

        self.assertEqual(respuesta.status_code, 200)
        usuarioTest = Usuario.objects.get(email='TestCorreo@test.com')
        jsonRespuestaVista = {
            'exito': True, 'Usuario con id': f'{usuarioTest.id}'
        }
        self.assertEqual(respuesta.json(),jsonRespuestaVista)

    def test_actualizar_usuario(self):
        usuarioTest = Usuario(
            nombre='TestNombre',
            apellido='TestApellido',
            email='TestCorreo@test.com'
        )
        usuarioTest.save()
        usuarioActualizar = {
            'nombre' : 'TestNombre2',
            'apellido' : 'TestApellido2',
            'email' : 'TestCorreo2@test.com'
        }

        respuesta = self.client.put(
            f'/gestion/usuarios/actualizar/{usuarioTest.id}',
            data=usuarioActualizar,
            content_type='application/json'
        )
        self.assertEqual(respuesta.status_code, 200)
        usuarioActualizado = Usuario.objects.get(id=usuarioTest.id)
        self.assertEqual('TestCorreo2@test.com',usuarioActualizado.email)

    def test_borrar_usuario(self):
        usuarioTest = Usuario(
            nombre='TestNombre',
            apellido='TestApellido',
            email='TestCorreo@test.com'
        )
        usuarioTest.save()
        respuesta = self.client.delete(f'/gestion/usuarios/borrar/{usuarioTest.id}')
        jsonRespuestaVista = {
                'exito': True,
                'mensaje': 'Usuario borrado correctamente'
            }
        #el with crea un bloque de codigo que espera algo en concreto, si salta el error bien, si no salta sale mal el test
        with self.assertRaises(Usuario.DoesNotExist):
            Usuario.objects.get(email='TestCorreo@test.com')
        self.assertEqual(respuesta.json(), jsonRespuestaVista)

class EquipoTest(TestCase):
    def test_asignar_equipo(self):
        usuarioTest = Usuario(
            nombre='TestNombre',
            apellido='TestApellido',
            email='TestCorreo@test.com'
        )
        usuarioTest.save()
        #Creacion de cartas para poder testear la funcion

        for i in range(10):
            CartaPortero.objects.create(
                nombre=f"PorteroTest {i}",
                posicion='POR',
                estirada=50, paradas=50, saque=50,
                reflejos=50, velocidad=50, colocacion=50
            )
        posiciones_def = ['DFC', 'LTI', 'LTD']
        posiciones_cen = ['MC', 'MI', 'MD']
        posiciones_del = ['DC', 'MP']

        for i in range(10):  # Crear 10 Defensas
            CartaJugador.objects.create(
                nombre=f"DefensaTest {i}",
                posicion=random.choice(posiciones_def),
                ritmo=50, tiro=50, pase=50,
                regate=50, defensa=50, fisico=50
            )
        for i in range(10):  # Crear 10 Centrocampistas
            CartaJugador.objects.create(
                nombre=f"CentroTest {i}",
                posicion=random.choice(posiciones_cen),
                ritmo=50, tiro=50, pase=50,
                regate=50, defensa=50, fisico=50
            )
        for i in range(10):  # Crear 10 Delanteros
            CartaJugador.objects.create(
                nombre=f"DelanteroTest {i}",
                posicion=random.choice(posiciones_del),
                ritmo=50, tiro=50, pase=50,
                regate=50, defensa=50, fisico=50
            )


        respuesta = self.client.post(f'/gestion/usuarios/{usuarioTest.id}/asignar')
        self.assertEqual(respuesta.status_code, 200)
        usuarioTestEquipo = Usuario.objects.get(email='TestCorreo@test.com')
        respuestaVista = {
                'exito': True,
                'equipo': usuarioTestEquipo.equipo.nombre,
                'id equipo': usuarioTestEquipo.equipo.id
                                 }
        self.assertEqual(respuesta.json(),respuestaVista)

    def test_listar_equipo(self):
        cartaTest = CartaPortero.objects.create(
            nombre="PorteroTest 1", posicion='POR', estirada=50, paradas=50,
            saque=50, reflejos=50, velocidad=50, colocacion=50
        )
        equipoTest = Equipo.objects.create(nombre="Equipo de Prueba")
        equipoTest.cartas.add(cartaTest)
        usuarioTest = Usuario(
            nombre='TestNombre',
            apellido='TestApellido',
            email='TestCorreo@test.com',
            equipo=equipoTest
        )
        usuarioTest.save()
        respuesta = self.client.get(f'/gestion/usuarios/{usuarioTest.id}/equipo')

        self.assertEqual(respuesta.status_code,200)
        datos_respuesta = respuesta.json()
        self.assertEqual(datos_respuesta['equipo'],equipoTest.nombre)

class CartaTest(TestCase):
    # ---------- MODELOS ----------

    def test_crear_carta_jugador_modelo(self):
        carta = CartaJugador(
            nombre='Jugador Test',
            pais='España',
            club='Test FC',
            liga='Liga Test',
            posicion='DC',
            ritmo=80,
            tiro=90,
            pase=70,
            regate=75,
            defensa=30,
            fisico=85
        )
        carta.save()

        carta_db = CartaJugador.objects.get(nombre='Jugador Test')

        # Se ha guardado bien el tipo y la valoración
        self.assertEqual(carta_db.tipo, 'JUG')
        self.assertGreaterEqual(carta_db.valoracion_general, 1)
        self.assertLessEqual(carta_db.valoracion_general, 99)

    def test_crear_carta_portero_modelo(self):
        carta = CartaPortero(
            nombre='Portero Test',
            pais='España',
            club='Test FC',
            liga='Liga Test',
            posicion='POR',
            estirada=80,
            paradas=85,
            saque=70,
            reflejos=90,
            velocidad=60,
            colocacion=88
        )
        carta.save()

        carta_db = CartaPortero.objects.get(nombre='Portero Test')

        self.assertEqual(carta_db.tipo, 'POR')
        self.assertGreaterEqual(carta_db.valoracion_general, 1)
        self.assertLessEqual(carta_db.valoracion_general, 99)

    def test_carta_jugador_valor_invalido_lanza_error(self):
        # ritmo fuera de rango (1-99) -> debe lanzar ValueError al guardar
        carta = CartaJugador(
            nombre='Jugador Malo',
            pais='España',
            club='Test FC',
            liga='Liga Test',
            posicion='DC',
            ritmo=150,
            tiro=90,
            pase=70,
            regate=75,
            defensa=30,
            fisico=85
        )
        with self.assertRaises(ValueError):
            carta.save()

    def test_carta_portero_posicion_invalida_lanza_error(self):
        # Un portero con posición que no sea POR debe romper
        carta = CartaPortero(
            nombre='Portero Raro',
            pais='España',
            club='Test FC',
            liga='Liga Test',
            posicion='DC',
            estirada=80,
            paradas=85,
            saque=70,
            reflejos=90,
            velocidad=60,
            colocacion=88
        )
        with self.assertRaises(ValueError):
            carta.save()

    # ---------- VISTAS ----------

    def test_crear_carta_vista_jugador(self):
        datos_carta = {
            "tipo": "JUG",
            "nombre": "Jugador Test Vista",
            "pais": "España",
            "club": "Test FC",
            "liga": "Liga Test",
            "posicion": "DC",
            "ritmo": 80,
            "tiro": 90,
            "pase": 70,
            "regate": 75,
            "defensa": 30,
            "fisico": 85
        }

        respuesta = self.client.post(
            '/gestion/cartas/crear/',
            data=json.dumps(datos_carta),
            content_type='application/json'
        )

        self.assertEqual(respuesta.status_code, 201)
        json_resp = respuesta.json()
        self.assertIn("id", json_resp)

        carta_db = CartaJugador.objects.get(id=json_resp["id"])
        self.assertEqual(carta_db.nombre, "Jugador Test Vista")
        self.assertEqual(carta_db.tipo, "JUG")

    def test_listar_cartas_solo_activas(self):
        # Creamos una carta activa y otra inactiva
        activa = CartaJugador.objects.create(
            nombre='Activa',
            pais='España',
            club='Test FC',
            liga='Liga Test',
            posicion='DC',
            ritmo=80,
            tiro=80,
            pase=80,
            regate=80,
            defensa=30,
            fisico=80
        )
        inactiva = CartaJugador.objects.create(
            nombre='Inactiva',
            pais='España',
            club='Test FC',
            liga='Liga Test',
            posicion='MC',
            ritmo=70,
            tiro=70,
            pase=70,
            regate=70,
            defensa=70,
            fisico=70
        )
        inactiva.activa = False
        inactiva.save()

        respuesta = self.client.get('/gestion/cartas/')
        self.assertEqual(respuesta.status_code, 200)

        data = respuesta.json()      # es una lista de dicts (values())
        # Solo debe haber 1 carta activa
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nombre'], 'Activa')

    def test_detalle_carta(self):
        carta = CartaJugador.objects.create(
            nombre='DetalleTest',
            pais='España',
            club='Test FC',
            liga='Liga Test',
            posicion='DC',
            ritmo=80,
            tiro=80,
            pase=80,
            regate=80,
            defensa=30,
            fisico=80
        )

        respuesta = self.client.get(f'/gestion/cartas/{carta.id}/')
        self.assertEqual(respuesta.status_code, 200)

        data = respuesta.json()
        # El string de detalle debe contener el nombre
        self.assertIn('DetalleTest', data['detalle'])

    def test_eliminar_carta_pone_activa_false(self):
        carta = CartaJugador.objects.create(
            nombre='CartaEliminar',
            pais='España',
            club='Test FC',
            liga='Liga Test',
            posicion='DC',
            ritmo=80,
            tiro=80,
            pase=80,
            regate=80,
            defensa=30,
            fisico=80
        )
        self.assertTrue(carta.activa)

        respuesta = self.client.post(f'/gestion/cartas/{carta.id}/eliminar/')
        self.assertEqual(respuesta.status_code, 200)

        carta_refrescada = Carta.objects.get(id=carta.id)
        self.assertFalse(carta_refrescada.activa)