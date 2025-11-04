import random
from faker import Faker
from django.core.management import BaseCommand
from gestion.models import CartaPortero, CartaJugador


class Command(BaseCommand):
    help = 'Crea 150 cartas al inicio'

    def handle(self, *args, **options):
        self.stdout.write('Creando Cartas')
        fake = Faker('es_ES')
        tipos_posicion = ['POR', 'DEF', 'CEN', 'DEL']
        pesos = [16, 56, 47, 31]  # (Esto es el porcentaje aproximado de tipos de jugadores en cada equipo)
        for _ in range(150):
            tipo = random.choices(tipos_posicion, weights=pesos, k=1)[0]
            nombre = fake.name_male()
            pais = fake.country()
            club = f"{fake.city()} {random.choice(['FC', 'United', 'CF', 'Rayo','Sporting','Real'])}"
            liga = f"Liga {fake.word().capitalize()}"


            match tipo:
                case 'POR':
                    estirada = random.randint(1, 99)
                    paradas = random.randint(1, 99)
                    saque = random.randint(1, 99)
                    reflejos = random.randint(1, 99)
                    velocidad = random.randint(1, 99)
                    colocacion = random.randint(1, 99)
                    carta = CartaPortero(
                        nombre=nombre,
                        pais=pais,
                        club=club,
                        liga=liga,
                        posicion='POR',
                        estirada=estirada,
                        paradas=paradas,
                        saque=saque,
                        reflejos=reflejos,
                        velocidad=velocidad,
                        colocacion=colocacion,
                    )
                    pass
                case 'DEF':
                    posicion_defensa = random.choice(['DFC','LTI','LTD'])
                    ritmo = random.randint(1, 99)
                    tiro = random.randint(1, 99)
                    pase = random.randint(1, 99)
                    regate = random.randint(1, 99)
                    defensa = random.randint(50, 99)
                    fisico = random.randint(1, 99)
                    carta = CartaJugador(
                        nombre=nombre,
                        pais=pais,
                        club=club,
                        liga=liga,
                        tipo='JUG',
                        posicion = posicion_defensa,
                        ritmo = ritmo,
                        tiro = tiro,
                        defensa = defensa,
                        fisico = fisico,
                        regate = regate,
                        pase = pase,
                    )
                    pass
                case 'CEN':
                    posicion_centrocampista = random.choice(['MC', 'MI', 'MD'])
                    ritmo = random.randint(1, 99)
                    tiro = random.randint(1, 99)
                    pase = random.randint(1, 99)
                    regate = random.randint(1, 99)
                    defensa = random.randint(1, 99)
                    fisico = random.randint(1, 99)
                    carta = CartaJugador(
                        nombre=nombre,
                        pais=pais,
                        club=club,
                        liga=liga,
                        tipo='JUG',
                        posicion=posicion_centrocampista,
                        ritmo=ritmo,
                        tiro=tiro,
                        defensa=defensa,
                        fisico=fisico,
                        regate=regate,
                        pase=pase,
                    )
                    pass
                case 'DEL':
                    posicion_delantero = random.choice(['MP', 'DC'])
                    ritmo = random.randint(1, 99)
                    tiro = random.randint(50, 99)
                    pase = random.randint(1, 99)
                    regate = random.randint(1, 99)
                    defensa = random.randint(1, 50)
                    fisico = random.randint(1, 99)
                    carta = CartaJugador(
                        nombre=nombre,
                        pais=pais,
                        club=club,
                        liga=liga,
                        tipo='JUG',
                        posicion=posicion_delantero,
                        ritmo=ritmo,
                        tiro=tiro,
                        defensa=defensa,
                        fisico=fisico,
                        regate=regate,
                        pase=pase,
                    )
                    pass
            carta.save()
            self.stdout.write(f'Carta creada con exito {carta.nombre}')
