from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Evento, Persona
from .serializers import EventoSerializer, PersonaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-fecha', 'hora_inicio']

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['apellido', 'nombre']