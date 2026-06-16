from django.db import models
from django.conf import settings

class PacienteClinico(models.Model):
    id_paciente = models.IntegerField(unique=True, db_column='id_paciente')
    nombres = models.CharField(max_length=150, db_column='nombres')
    apellidos = models.CharField(max_length=150, db_column='apellidos')
    edad = models.IntegerField(db_column='edad')
    sexo = models.CharField(max_length=20, db_column='sexo')
    peso = models.FloatField(db_column='peso')
    altura = models.FloatField(db_column='altura')
    IMC = models.FloatField(db_column='IMC')
    presion_sistolica = models.IntegerField(db_column='presión_sistólica')
    presion_diastolica = models.IntegerField(db_column='presión_diastólica')
    frecuencia_cardiaca = models.IntegerField(db_column='frecuencia_cardiaca')
    glucosa = models.FloatField(db_column='glucosa')
    colesterol = models.FloatField(db_column='colesterol')
    saturacion_oxigeno = models.FloatField(db_column='saturación_oxígeno')
    temperatura = models.FloatField(db_column='temperatura')
    antecedentes_familiares = models.BooleanField(db_column='antecedentes_familiares')
    fumador = models.BooleanField(db_column='fumador')
    consumo_alcohol = models.BooleanField(db_column='consumo_alcohol')
    actividad_fisica = models.CharField(max_length=100, db_column='actividad_física')
    diagnostico_preliminar = models.CharField(max_length=250, db_column='diagnóstico_preliminar')
    riesgo_enfermedad = models.CharField(max_length=50, db_column='riesgo_enfermedad')
    fecha_consulta = models.DateField(db_column='fecha_consulta')

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.id_paciente})"


class RegistroETL(models.Model):
    ESTADO_CHOICES = [
        ('exitoso', 'Exitoso'),
        ('fallido', 'Fallido'),
    ]

    fecha = models.DateTimeField(auto_now_add=True)
    usuario_fk = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registros_etl'
    )
    registros_procesados = models.IntegerField()
    registros_limpios = models.IntegerField()
    duplicados_eliminados = models.IntegerField()
    tiempo_ejecucion = models.FloatField()  # En segundos
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    errores = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"ETL {self.id} - {self.fecha.strftime('%Y-%m-%d %H:%M')} - {self.estado}"

