from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Evento, Persona
from .serializers import EventoSerializer, PersonaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response  # <-- Añade esta línea
from django.db.models import Count

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['estado']  # Permite filtrar por estado
    ordering_fields = '__all__'
    ordering = ['-fecha', 'hora_inicio']

    def perform_create(self, serializer):
        # Actualizar el estado antes de guardar
        instance = serializer.save(creado_por=self.request.user)
        instance.save()  # Esto activará la actualización del estado

    queryset = Evento.objects.annotate(
        participantes_count=Count('participantes')
    )
    @action(detail=True, methods=['post'])
    def actualizar_estado(self, request, pk=None):
        evento = self.get_object()
        nuevo_estado = evento.actualizar_estado()
        return Response({'estado': nuevo_estado})
    
    @action(detail=False, methods=['post'])
    def actualizar_estados(self, request):
        eventos = Evento.objects.all()
        for evento in eventos:
            evento.actualizar_estado()
        
        serializer = self.get_serializer(eventos, many=True)
        return Response(serializer.data)
    
class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['eventos']  # <-- Añade este filtro
    ordering_fields = '__all__'
    ordering = ['apellido', 'nombre']