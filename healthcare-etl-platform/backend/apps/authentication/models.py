from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ADMINISTRADOR = 'administrador'
    MEDICO = 'medico'
    ANALISTA = 'analista'

    ROLE_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (MEDICO, 'Médico'),
        (ANALISTA, 'Analista'),
    ]

    rol = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ANALISTA
    )

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

