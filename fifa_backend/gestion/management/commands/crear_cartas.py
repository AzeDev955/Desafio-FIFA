import random
from faker import Faker
from django.core.management import BaseCommand
from gestion.models import *

from fifa_backend.gestion.models import CartaPortero


class Command(BaseCommand):
    help = 'Crea 150 cartas al inicio'

    def handle(self, *args, **options):
        self.stdout.write('Creando Cartas')
        fake = Faker('es_ES')
        tipos_posicion = ['POR', 'DEF', 'CEN', 'DEL']
        pesos = [16, 56, 47, 31]  # (Esto es el porcentaje aproximado de tipos de jugadores en cada equipo)
        for _ in range(150):
            tipo = random.choice(tipos_posicion, weights=pesos, k=1)[0]
            nombre = fake.name_male()
            pais = fake.country()
            club = f"{fake.city()} {random.choice(['FC', 'United', 'CF', 'Rayo','Sporting','Real'])}"
            liga = f"Liga {fake.word().capitalize()}"


            match tipo:
                case 'POR':
                    estirada = random.randint(1, 100)
                    paradas = random.randint(1, 100)
                    saque = random.randint(1, 100)
                    reflejos = random.randint(1, 100)
                    velocidad = random.randint(1, 100)
                    colocacion = random.randint(1, 100)
                    carta = CartaPortero()
                    pass
                case 'DEF':
                    ritmo = random.randint(1, 100)
                    tiro = random.randint(1, 100)
                    pase = random.randint(1, 100)
                    regate = random.randint(1, 100)
                    defensa = random.randint(50, 100)
                    fisico = random.randint(1, 100)
                    pass
                case 'CEN':
                    ritmo = random.randint(1, 100)
                    tiro = random.randint(1, 100)
                    pase = random.randint(1, 100)
                    regate = random.randint(1, 100)
                    defensa = random.randint(1, 100)
                    fisico = random.randint(1, 100)
                    pass
                case 'DEL':
                    ritmo = random.randint(1, 100)
                    tiro = random.randint(50, 100)
                    pase = random.randint(1, 100)
                    regate = random.randint(1, 100)
                    defensa = random.randint(1, 50)
                    fisico = random.randint(1, 100)
                    pass
