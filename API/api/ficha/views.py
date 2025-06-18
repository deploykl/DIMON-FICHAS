from django.shortcuts import render
from django.db.models import Count
from datetime import datetime

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema, extend_schema_view  # type: ignore
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from rest_framework.filters import OrderingFilter
from api.ficha.serializers import *

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
class ProcesoViewSet(viewsets.ModelViewSet):
    queryset = Proceso.objects.all()
    serializer_class = ProcesoSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
 
    def get_queryset(self):
        categoria_id = self.request.query_params.get('categoria_id')
        if categoria_id:
            return Proceso.objects.filter(categoria_id=categoria_id)
        return Proceso.objects.all()
       
class SubprocesoViewSet(viewsets.ModelViewSet):
    queryset = Subproceso.objects.all()
    serializer_class = SubprocesoSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
class VerificadorViewSet(viewsets.ModelViewSet):
    queryset = Verificador.objects.all()
    serializer_class = VerificadorSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
class EvaluacionVerificadorViewSet(viewsets.ModelViewSet):
    queryset = EvaluacionVerificador.objects.all()
    serializer_class = EvaluacionVerificadorSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["-fecha_evaluacion"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
    def perform_create(self, serializer):
        # Asigna automáticamente el usuario actual al crear una evaluación
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def por_verificador(self, request):
        verificador_id = request.query_params.get('verificador_id')
        if not verificador_id:
            return Response(
                {"error": "Se requiere el parámetro verificador_id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        evaluaciones = self.get_queryset().filter(verificador_id=verificador_id)
        serializer = self.get_serializer(evaluaciones, many=True)
        return Response(serializer.data)
    
