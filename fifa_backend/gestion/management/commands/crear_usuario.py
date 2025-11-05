from django.core.management.base import BaseCommand
from faker import Faker
from gestion.models import Usuario

class Command(BaseCommand):
    help = "Crea 30 usuarios sin equipo"

    def handle(self, *args, **options):
        fake = Faker("es_ES")
        self.stdout.write("Creando usuarios...")
        for _ in range(30):
            usuario = Usuario.objects.create(
                nombre=fake.first_name(),
                apellido=fake.last_name(),
                email=fake.unique.email(),
            )
            self.stdout.write(f"Usuario creado: {usuario.id} - {usuario.email}")
        self.stdout.write(self.style.SUCCESS("✅ Creados 30 usuarios correctamente"))
