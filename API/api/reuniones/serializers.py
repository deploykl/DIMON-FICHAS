from rest_framework import serializers
from .models import Evento, Persona

class EventoSerializer(serializers.ModelSerializer):
    creado_por = serializers.StringRelatedField()  # Muestra el username del usuario
    
    class Meta:
        model = Evento
        fields = '__all__'
        read_only_fields = ('creado_en', 'creado_por')

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