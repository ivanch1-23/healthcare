from rest_framework import serializers
from .models import PacienteClinico, RegistroETL

class PacienteClinicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteClinico
        fields = '__all__'


class RegistroETLSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='usuario_fk.username', read_only=True)

    class Meta:
        model = RegistroETL
        fields = (
            'id', 
            'fecha', 
            'usuario_username', 
            'registros_procesados', 
            'registros_limpios', 
            'duplicados_eliminados', 
            'tiempo_ejecucion', 
            'estado', 
            'errores'
        )
