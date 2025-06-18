from rest_framework import serializers
from .models import *


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

class EvaluacionVerificadorSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    verificador_nombre = serializers.CharField(source='verificador.descripcion', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = EvaluacionVerificador
        fields = '__all__'
        extra_kwargs = {
            'usuario': {'read_only': True},
            'fecha_evaluacion': {'read_only': True}
        }
        
class MatrizCompromisoSerializer(serializers.ModelSerializer):
    evaluacion_data = serializers.SerializerMethodField()
    
    class Meta:
        model = MatrizCompromiso
        fields = '__all__'
        read_only_fields = ('fecha_creacion',)
    
    def get_evaluacion_data(self, obj):
        evaluacion = obj.evaluacion
        return {
            'tipo': evaluacion.get_tipo_display(),
            'establecimiento': evaluacion.establecimiento,
            'proceso_nombre': evaluacion.verificador.subproceso.proceso.nombre_proceso,
            'categoria': evaluacion.verificador.subproceso.proceso.categoria.name,
            'fecha_monitoreo': evaluacion.fecha_evaluacion,
            'dueño_proceso': evaluacion.verificador.subproceso.proceso.dueño_proceso,
            'subproceso_nombre': evaluacion.verificador.subproceso.nombre,
            'verificador_descripcion': evaluacion.verificador.descripcion,
            'estado': evaluacion.get_estado_display(),
            'usuario': evaluacion.usuario.get_full_name() or evaluacion.usuario.username
        }