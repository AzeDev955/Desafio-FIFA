from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    equipo = models.OneToOneField('Equipo', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.nombre} {self.apellido}}"



class Equipo(models.Model):
    nombre = models.CharField(max_length=150)

    cartas = models.ManyToManyField(
        'Carta',
        blank=True
    )
    def __str__(self):
        return f"{self.nombre}"

class Carta(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=50, blank=True)
    club = models.CharField(max_length=100, blank=True)
    liga = models.CharField(max_length=100, blank=True)

    ritmo = models.IntegerField()
    tiro = models.IntegerField()
    pase = models.IntegerField()
    regate = models.IntegerField()
    defensa = models.IntegerField()
    fisico = models.IntegerField()

    activa = models.BooleanField(default=True)
    valoracion_general = models.IntegerField( editable=False, null=False)

    posiciones = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
    ]

    def __str__(self):
        return f"{self.nombre}, {self.valoracion_general}"