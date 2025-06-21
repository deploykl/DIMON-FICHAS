from rest_framework import serializers
from .models import *


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class ProcesoSerializer(serializers.ModelSerializer):
    categoria_name = serializers.CharField(source="categoria.name")
    categoria_tipo = serializers.CharField(source="categoria.tipo")  # Nuevo campo

    class Meta:
        model = Proceso
        fields = "__all__"

class SubprocesoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subproceso
        fields = "__all__"


class VerificadorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Verificador
        fields = "__all__"
        extra_kwargs = {"orden": {"required": False}}


class EvaluacionVerificadorSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    verificador_nombre = serializers.CharField(
        source="verificador.descripcion", read_only=True
    )
    usuario_nombre = serializers.CharField(
        source="usuario.get_full_name", read_only=True
    )
    subproceso_nombre = serializers.CharField(
        source="verificador.subproceso.nombre", read_only=True
    )
    subproceso_nivel = serializers.CharField(
        source="verificador.subproceso.nivel", read_only=True
    )
    subproceso_codigo = serializers.SerializerMethodField()

    class Meta:
        model = EvaluacionVerificador
        fields = "__all__"
        extra_kwargs = {
            "usuario": {"read_only": True},
            "fecha_evaluacion": {"read_only": True},
        }

    def get_subproceso_codigo(self, obj):
        return (
            f"PS{obj.verificador.subproceso.proceso.id}.{obj.verificador.subproceso.id}"
        )


class MatrizCompromisoSerializer(serializers.ModelSerializer):
    evaluacion_data = serializers.SerializerMethodField()
    evaluaciones_nc = EvaluacionVerificadorSerializer(many=True, read_only=True)
    monitor_nombre = serializers.SerializerMethodField()  # Nuevo campo
    todas_evaluaciones = serializers.SerializerMethodField()

    class Meta:
        model = MatrizCompromiso
        fields = "__all__"
        extra_kwargs = {
            "firma_a": {"required": False, "allow_null": True},
            "firma_b": {"required": False, "allow_null": True},
            "firma_c": {"required": False, "allow_null": True},
            "firma_d": {"required": False, "allow_null": True},
            "firma_e": {"required": False, "allow_null": True},
        }

    def get_monitor_nombre(self, obj):
        # Obtener el nombre del usuario que creó la evaluación
        if obj.evaluacion and obj.evaluacion.usuario:
            return f"{obj.evaluacion.usuario.first_name} {obj.evaluacion.usuario.last_name}"
        return ""

    def get_evaluacion_data(self, obj):
        evaluacion = obj.evaluacion
        return {
            "tipo": evaluacion.get_tipo_display(),
            "establecimiento": evaluacion.establecimiento,
            "fecha_monitoreo": evaluacion.fecha_evaluacion,
            "proceso_nombre": evaluacion.verificador.subproceso.proceso.nombre_proceso,
            "categoria": evaluacion.verificador.subproceso.proceso.categoria.tipo,
            "dueño_proceso": evaluacion.verificador.subproceso.proceso.dueño_proceso,
            "estado": evaluacion.get_estado_display(),
            
            "monitor_nombre": self.get_monitor_nombre(obj),
            "subproceso_nombre": evaluacion.verificador.subproceso.nombre,
            "verificador_descripcion": evaluacion.verificador.descripcion,
            "total_nc": obj.evaluaciones_nc.count(),
            "subprocesos_afectados": list(
                set(
                    nc.verificador.subproceso.nombre for nc in obj.evaluaciones_nc.all()
                )
            ),
        }
# En MatrizCompromisoSerializer
    def get_todas_evaluaciones(self, obj):
        # Obtener todas las evaluaciones asociadas a esta matriz
        evaluaciones = list(obj.evaluaciones_nc.all())
        return EvaluacionVerificadorSerializer(evaluaciones, many=True).data
