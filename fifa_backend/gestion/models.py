from django.db import models
from django.db.models import Q
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    equipo = models.OneToOneField('Equipo', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Equipo(models.Model):
    nombre = models.CharField(max_length=150)

    cartas = models.ManyToManyField(
        'Carta',
        blank=True
    )
    def __str__(self):
        return f"{self.nombre}"

class Carta(models.Model):
    TIPO_CHOICES = [
        ('JUG', 'Jugador de campo'),
        ('POR', 'Portero'),
    ]

    POSICION_CHOICES = [
        ('POR', 'Portero'),
        ('DFC', 'Defensa Central'),
        ('LTI', 'Lateral Izquierdo'),
        ('LTD', 'Lateral Derecho'),
        ('MC',  'Medio Centro'),
        ('MI',  'Medio Izquierdo'),
        ('MD',  'Medio Derecho'),
        ('DC',  'Delantero Centro'),
        ('MP',  'Media Punta'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    pais = models.CharField(max_length=50, blank=True)
    club = models.CharField(max_length=100, blank=True)
    liga = models.CharField(max_length=100, blank=True)
    activa = models.BooleanField(default=True)
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES, editable=False)
    posicion = models.CharField(max_length=3, choices=POSICION_CHOICES)
    valoracion_general = models.IntegerField(editable=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f"{self.nombre} · {self.get_posicion_display()} · {self.club} · {self.pais} · OVR {self.valoracion_general}"
    
    class Meta:
        ordering = ['-valoracion_general', 'nombre']
        constraints = [
            models.CheckConstraint(
                name='tipo_por_pos_por',
                check=Q(tipo='POR', posicion='POR') | ~Q(tipo='POR')
            ),
            models.CheckConstraint(
                name='tipo_jug_pos_no_por',
                check=Q(tipo='JUG') & ~Q(posicion='POR') | ~Q(tipo='JUG')
            ),
        ]

        

class CartaJugador(Carta):
    ritmo = models.IntegerField()
    tiro = models.IntegerField()
    pase = models.IntegerField()
    regate = models.IntegerField()
    defensa = models.IntegerField()
    fisico = models.IntegerField()

    pesos = {
        'DC':  {'ritmo': 0.45, 'tiro': 0.45, 'pase': 0.05, 'regate': 0.05},
        'MP':  {'ritmo': 0.40, 'tiro': 0.25, 'pase': 0.20, 'regate': 0.15},
        'MC':  {'ritmo': 0.20, 'tiro': 0.20, 'pase': 0.25, 'regate': 0.25, 'defensa': 0.10},
        'LTI': {'ritmo': 0.20, 'tiro': 0.10, 'pase': 0.20, 'regate': 0.20, 'defensa': 0.30},
        'LTD': {'ritmo': 0.20, 'tiro': 0.10, 'pase': 0.20, 'regate': 0.20, 'defensa': 0.30},
        'DFC': {'ritmo': 0.10, 'tiro': 0.05, 'pase': 0.15, 'regate': 0.10, 'defensa': 0.60},
        'MI':  {'ritmo': 0.40, 'tiro': 0.25, 'pase': 0.20, 'regate': 0.15},
        'MD':  {'ritmo': 0.40, 'tiro': 0.25, 'pase': 0.20, 'regate': 0.15},
    }

    def save(self, *args, **kwargs):
        if self.posicion == 'POR':
            raise ValueError("Las cartas de jugador no pueden tener posición 'POR'.")

        for campo in ['ritmo', 'tiro', 'pase', 'regate', 'defensa', 'fisico']:
            valor = getattr(self, campo)
            if not 1 <= valor <= 99:
                raise ValueError(f"{campo} debe estar entre 1 y 99 (valor recibido: {valor})")
            
        self.tipo = 'JUG'
        p = self.pesos.get(self.posicion)
        if not p:
            raise ValueError(f"No hay pesos definidos para la posición '{self.posicion}'.")

        if abs(sum(p.values()) - 1.0) > 1e-6:
            ##con esta parte nos aseguramos que si el valor es 0.999999 o 1.0000001 no dara error
            raise ValueError(f"Los pesos de '{self.posicion}' no suman 1.0: {sum(p.values())}")

        media = sum(getattr(self, stat) * peso for stat, peso in p.items())
        self.valoracion_general = max(1, min(99, int(round(media))))
        super().save(*args, **kwargs)

    def __str__(self):
        base = super().__str__()
        return (
            f"{base} · [RIT {self.ritmo} | TIR {self.tiro} | PAS {self.pase} | "
            f"REG {self.regate} | DEF {self.defensa} | FIS {self.fisico}]"
            )


class CartaPortero(Carta):
    estirada = models.IntegerField()
    paradas = models.IntegerField()
    saque = models.IntegerField()
    reflejos = models.IntegerField()
    velocidad = models.IntegerField()
    colocacion = models.IntegerField()

    pesos = {
        'POR': {
            'estirada':   0.22,
            'paradas':    0.22,
            'saque':      0.07,
            'reflejos':   0.22,
            'velocidad':  0.05,
            'colocacion': 0.22,
        }
    }

    def save(self, *args, **kwargs):
        if self.posicion != 'POR':
            raise ValueError("Las cartas de portero deben tener posición 'POR'.")

        for campo in ['estirada', 'paradas', 'saque', 'reflejos', 'velocidad', 'colocacion']:
            valor = getattr(self, campo)
            if not 1 <= valor <= 99:
                raise ValueError(f"{campo} debe estar entre 1 y 99 (valor recibido: {valor})")
            
        self.tipo = 'POR'
        p = self.pesos.get('POR')
        if not p:
            raise ValueError("No hay pesos definidos para 'POR'.")

        if abs(sum(p.values()) - 1.0) > 1e-6:
            raise ValueError(f"Los pesos de 'POR' no suman 1.0: {sum(p.values())}")

        media = (
            self.estirada   * p['estirada']   +
            self.paradas    * p['paradas']    +
            self.saque      * p['saque']      +
            self.reflejos   * p['reflejos']   +
            self.velocidad  * p['velocidad']  +
            self.colocacion * p['colocacion']
        )

        self.valoracion_general = max(1, min(99, int(round(media))))
        super().save(*args, **kwargs)

    def __str__(self):
        base = super().__str__()
        return (
                f"{base} · [DIV {self.estirada} | HAN {self.paradas} | KIC {self.saque} | "
                f"REF {self.reflejos} | SPE {self.velocidad} | POS {self.colocacion}]"
        )