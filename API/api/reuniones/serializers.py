from rest_framework import serializers
from .models import Evento, Persona

class EventoSerializer(serializers.ModelSerializer):
    creado_por = serializers.SerializerMethodField()  # Cambia esto de StringRelatedField a SerializerMethodField
    fecha_local = serializers.SerializerMethodField()
    hora_inicio_local = serializers.SerializerMethodField()
    hora_fin_local = serializers.SerializerMethodField()
    estado_display = serializers.SerializerMethodField()
    participantes_count = serializers.IntegerField(read_only=True)  # Cambia esto

    class Meta:
        model = Evento
        fields = '__all__'
        read_only_fields = ('creado_en', 'creado_por', 'estado')
    
    def get_fecha_local(self, obj):
        return obj.fecha.strftime('%Y-%m-%d')
    
    def get_hora_inicio_local(self, obj):
        return obj.hora_inicio.strftime('%H:%M')
    
    def get_hora_fin_local(self, obj):
        return obj.hora_fin.strftime('%H:%M')
    
    def get_estado_display(self, obj):
        return obj.get_estado_display()

    def validate(self, data):
        # Solo validar si estamos creando (no actualizando)
        if self.instance is None:
            dni = data.get('dni')
            eventos_ids = [evento.id for evento in data.get('eventos', [])]

            # Verificar para cada evento en la solicitud
            for evento_id in eventos_ids:
                evento = Evento.objects.get(id=evento_id)

                # Si el evento ya comenzó o finalizó
                if evento.estado != 'PENDIENTE':
                    # Verificar si ya existe una persona con este DNI en este evento
                    if Persona.objects.filter(
                        dni=dni,
                        eventos__id=evento_id
                    ).exists():
                        raise serializers.ValidationError(
                            f'Ya existe un participante con DNI {dni} registrado en este evento (ID: {evento_id})'
                        )

        return data
    def get_participantes_count(self, obj):
        return obj.participantes.count()  # <-- Esto ahora es correcto porque estamos en Evento
    
    def get_creado_por(self, obj):
        # Obtiene el nombre completo del usuario y lo formatea
        user = obj.creado_por
        if not user:
            return ""
        
        # Divide el nombre completo en partes
        parts = user.get_full_name().split()
        if not parts:
            return ""
        
        # Formatea el nombre en el formato deseado (Primera palabra + inicial segunda palabra)
        formatted_name = parts[0]
        if len(parts) > 1:
            formatted_name += f" {parts[1][0]}." if parts[1] else ""
        
        # Si hay más partes (apellidos), agrega el primer apellido completo y la inicial del segundo si existe
        if len(parts) > 2:
            formatted_name += f" {parts[2]}"
            if len(parts) > 3:
                formatted_name += f" {parts[3][0]}." if parts[3] else ""
        
        return formatted_name    
class PersonaSerializer(serializers.ModelSerializer):
    eventos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Evento.objects.all(),
        required=False
    )
    firma_url = serializers.SerializerMethodField()

    class Meta:
        model = Persona
        fields = '__all__'
        read_only_fields = ('fecha_registro',)

    def get_firma_url(self, obj):
        if obj.firma:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.firma.url)
        return None
    