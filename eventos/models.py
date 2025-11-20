from django.db import models
from django.conf import settings

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='eventos'
    )

    def __str__(self):
        return self.nombre


class Participante(models.Model):
    evento = models.ForeignKey(Evento, related_name="participantes", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()

    def __str__(self):
        return f"{self.nombre} ({self.correo})"
