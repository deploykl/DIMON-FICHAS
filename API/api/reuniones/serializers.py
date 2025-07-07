from rest_framework import serializers
from .models import Evento, Persona

class EventoSerializer(serializers.ModelSerializer):
    creado_por = serializers.StringRelatedField()
    fecha_local = serializers.SerializerMethodField()
    hora_inicio_local = serializers.SerializerMethodField()
    hora_fin_local = serializers.SerializerMethodField()
    
    class Meta:
        model = Evento
        fields = '__all__'
        read_only_fields = ('creado_en', 'creado_por')
    
    def get_fecha_local(self, obj):
        return obj.fecha.strftime('%Y-%m-%d')  # Ya está en la zona correcta por USE_TZ
    
    def get_hora_inicio_local(self, obj):
        return obj.hora_inicio.strftime('%H:%M')
    
    def get_hora_fin_local(self, obj):
        return obj.hora_fin.strftime('%H:%M')

class PersonaSerializer(serializers.ModelSerializer):
    eventos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Evento.objects.all(),
        required=False
    )    
    class Meta:
        model = Persona
        fields = '__all__'
        read_only_fields = ('fecha_registro',)