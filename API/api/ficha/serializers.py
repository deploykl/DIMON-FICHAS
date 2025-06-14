from rest_framework import serializers
from .models import (
    Institucion, 
    Categoria, 
    Proceso, 
    Subproceso, 
    Verificador
)

class InstitucionSerializer(serializers.ModelSerializer):
    #tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Institucion
        fields = '__all__'
        extra_kwargs = {
            'codigo': {'validators': []},  # Para updates sin validar unicidad
        }

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProcesoSerializer(serializers.ModelSerializer):
    #categoria_nombre = serializers.CharField(source='categoria.name', read_only=True)
    
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
