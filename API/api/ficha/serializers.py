from rest_framework import serializers
from .models import *
from datetime import datetime
from django.utils.timezone import make_aware


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
    codigo = serializers.CharField(source='evaluacion.codigo', read_only=True)
    contadores_evaluaciones = serializers.SerializerMethodField()

    class Meta:
        model = MatrizCompromiso
        fields = "__all__"
        extra_kwargs = {
            "firma_m": {"required": False, "allow_null": True},
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
    
    def get_contadores_evaluaciones(self, obj):
        # Obtener todas las evaluaciones asociadas a esta matriz
        evaluaciones = obj.evaluaciones_nc.all()
        
        return {
            'total_nc': evaluaciones.filter(estado='NC').count(),
            'total_na': evaluaciones.filter(estado='NA').count(),
            'total_c': evaluaciones.filter(estado='C').count(),
            'total': evaluaciones.count()
        }

class SeguimientoMatrizCompromisoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.SerializerMethodField()
    matriz = MatrizCompromisoSerializer(read_only=True)
    matriz_id = serializers.PrimaryKeyRelatedField(
        queryset=MatrizCompromiso.objects.all(), 
        source='matriz',
        write_only=True,
        required=False  # Asegúrate que esto esté presente
    )

    class Meta:
        model = SeguimientoMatrizCompromiso
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'usuario_creacion']  # Añade 'usuario_creacion' aquí

    def validate(self, data):
        matriz = data.get('matriz')
        
        # Para actualizaciones, usa la matriz existente
        if self.instance and not matriz:
            matriz = self.instance.matriz
            
        if not matriz:
            raise serializers.ValidationError("Se requiere una matriz para el seguimiento.")
            
        # Solo valida la fecha si está en los datos
        if 'fecha_seguimiento' in data and data['fecha_seguimiento'] < matriz.fecha_creacion.date():
            raise serializers.ValidationError(
                "La fecha de seguimiento no puede ser anterior a la creación de la matriz."
            )
            
        return data

    def get_matriz_data(self, obj):
        return {
            'establecimiento': obj.matriz.evaluacion.establecimiento,
            'codigo': obj.matriz.evaluacion.codigo,
            'categoria': obj.matriz.evaluacion.categoria
        }
    def get_usuario_nombre(self, obj):
        if obj.usuario_creacion:
            return f"{obj.usuario_creacion.first_name} {obj.usuario_creacion.last_name}"
        return "N/A"  # Cambiado de "Sistema" a "N/A" para mayor claridad
    

class AlertasSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    fecha_creacion = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    usuario_nombre = serializers.SerializerMethodField()
    total_seguimientos = serializers.SerializerMethodField()

    class Meta:
        model = Alertas
        fields = ['id', 'codigo', 'tipo', 'descripcion', 'fecha_creacion', 
                 'usuario', 'usuario_nombre', 'total_seguimientos']
        read_only_fields = ('id', 'codigo', 'fecha_creacion', 'usuario', 'usuario_nombre', 'total_seguimientos')

    def get_usuario_nombre(self, obj):
        if obj.usuario:
            return f"{obj.usuario.first_name} {obj.usuario.last_name}"
        return "N/A"

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

    def get_total_seguimientos(self, obj):
        # Usamos len() en lugar de count() porque ya está precargado con prefetch_related
        return len(obj.seguimientos.all())
    
class SeguimientoAlertasSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.SerializerMethodField()
    alerta = AlertasSerializer(read_only=True)
    alerta_id = serializers.PrimaryKeyRelatedField(
        queryset=Alertas.objects.all(), 
        source='alerta',
        write_only=True,
        required=False  # Cambiado a requerido
    )

    class Meta:
        model = SeguimientoAlertas
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'usuario_creacion']

    def validate(self, data):
        alerta = data.get('alerta')
        
        if self.instance and not alerta:
            alerta = self.instance.alerta
            
        if not alerta:
            raise serializers.ValidationError("Se requiere una alerta para el seguimiento.")
            
        if 'fecha_seguimiento' in data:
            # Convertir a zona horaria local si es necesario
            if isinstance(data['fecha_seguimiento'], str):
                try:
                    fecha_naive = datetime.strptime(data['fecha_seguimiento'], '%Y-%m-%dT%H:%M:%S')
                    data['fecha_seguimiento'] = make_aware(fecha_naive)
                except ValueError:
                    raise serializers.ValidationError(
                        {"fecha_seguimiento": "Formato de fecha inválido. Use YYYY-MM-DDTHH:MM:SS"}
                    )
            
            if data['fecha_seguimiento'] < alerta.fecha_creacion:
                raise serializers.ValidationError(
                    {"fecha_seguimiento": "La fecha de seguimiento no puede ser anterior a la creación de la alerta."}
                )
            
        return data

    def get_alerta_data(self, obj):
        return {
            'codigo': obj.alertas.codigo,
            'tipo': obj.alertas.tipo,
            'descripcion': obj.alertas.descripcion
        }
        
    def get_usuario_nombre(self, obj):
        if obj.usuario_creacion:
            return f"{obj.usuario_creacion.first_name} {obj.usuario_creacion.last_name}"
        return "N/A"