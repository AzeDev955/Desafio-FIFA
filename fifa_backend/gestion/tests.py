from django.test import TestCase
from .models import *
import faker as fake

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

