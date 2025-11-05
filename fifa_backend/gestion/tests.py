from django.test import TestCase
from models import *
import faker as fake
# Create your tests here.
fake = fake.Faker('es_ES')

class UsuarioTest(TestCase):
    def test_crear_usuario(self):
        usuario = Usuario(
            nombre = 'TestNombre',
            apellido = 'TestApellido',
            email = 'TestCorreo@test.com'
        )
        usuario.save()

        usuarioTest = Usuario.objects.get(email='TestCorreo@test.com')

        self.assertEqual(usuario.email,usuarioTest.email)