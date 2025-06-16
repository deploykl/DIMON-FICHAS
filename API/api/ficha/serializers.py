from rest_framework import serializers
from .models import (
    Categoria, 
    Proceso, 
    Subproceso, 
    Verificador
)


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProcesoSerializer(serializers.ModelSerializer):
    categoria_name = serializers.CharField(source='categoria.name')  # Cambia 'nombre' a 'name'
    
    class Meta:
        model = Proceso
        fields = '__all__'

class SubprocesoSerializer(serializers.ModelSerializer):
    #nivel_display = serializers.CharField(source='get_nivel_display', read_only=True)
    #proceso_nombre = serializers.CharField(source='proceso.nombre', read_only=True)
    
    class Meta:
        model = Subproceso
        fields = '__all__'

class VerificadorSerializer(serializers.ModelSerializer):
    #subproceso_nombre = serializers.CharField(source='subproceso.nombre', read_only=True)
    
    class Meta:
        model = Verificador
        fields = '__all__'
        extra_kwargs = {
            'orden': {'required': False}
        }
