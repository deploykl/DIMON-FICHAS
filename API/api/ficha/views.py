from django.shortcuts import render
from django.db.models import Count
from datetime import datetime
import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

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
    
class MatrizCompromisoViewSet(viewsets.ModelViewSet):
    parser_classes = [JSONParser, MultiPartParser, FormParser]  # Add JSONParser

    
    queryset = MatrizCompromiso.objects.all().prefetch_related(
        'evaluaciones_nc__verificador__subproceso__proceso',
        'evaluaciones_nc__usuario'
    )
    serializer_class = MatrizCompromisoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['evaluacion']
    ordering_fields = '__all__'    
    serializer_class = MatrizCompromisoSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        evaluacion_id = self.request.query_params.get('evaluacion_id')
        if evaluacion_id:
            queryset = queryset.filter(evaluacion_id=evaluacion_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def por_evaluacion(self, request):
        evaluacion_id = request.query_params.get('evaluacion_id')
        if not evaluacion_id:
            return Response(
                {'error': 'Se requiere el parámetro evaluacion_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            evaluacion = EvaluacionVerificador.objects.get(id=evaluacion_id)
            if evaluacion.estado != 'NC':
                return Response(
                    {'error': 'Solo se puede crear matriz para evaluaciones que no cumplen'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            matriz, created = MatrizCompromiso.objects.get_or_create(
                evaluacion=evaluacion,
                defaults={
                    'descripcion_situacional': '',
                    'semaforo': 'Rojo',  # Valor por defecto
                    'riesgo_identificado': '',
                    'medidas_correctivas': '',
                    'hito_esperado': '',
                    'responsable_directo': '',
                    'plazo_inicio': None,
                    'plazo_fin': None,
                    'funcionario_depen_directo': '',
                    'funcionario_depen_indirecto': '',
                    'firmas_adicionales': ''
                }
            )
            
            serializer = self.get_serializer(matriz)
            return Response(serializer.data)
            
        except EvaluacionVerificador.DoesNotExist:
            return Response(
                {'error': 'Evaluación no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
            
    @action(detail=False, methods=['post'])
    def generar_completa(self, request):
        evaluaciones_ids = request.data.get('evaluaciones_ids', [])
        
        try:
            evaluaciones_nc = EvaluacionVerificador.objects.filter(
                id__in=evaluaciones_ids,
                estado='NC'
            ).select_related(
                'verificador__subproceso__proceso',
                'usuario'
            )
            
            if not evaluaciones_nc.exists():
                return Response(
                    {'error': 'No se encontraron evaluaciones No Conformes'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Crear matriz con la primera evaluación como referencia
            primera_eval = evaluaciones_nc.first()
            matriz = MatrizCompromiso.objects.create(
                evaluacion=primera_eval,
                descripcion_situacional='Múltiples verificadores no cumplen',
                semaforo='Rojo',
                riesgo_identificado='Riesgos identificados en los verificadores evaluados',
                medidas_correctivas='Plan de acción integral',
                hito_esperado='Cumplimiento de los verificadores',
                responsable_directo='',  # Ahora vacío por defecto
                plazo_inicio=datetime.now().date(),
                plazo_fin=datetime.now().date() + timedelta(days=30),
                funcionario_depen_directo='Por definir',
                funcionario_depen_indirecto='Por definir',
                firmas_adicionales=''
            )
            
            # Asociar evaluaciones NC
            matriz.evaluaciones_nc.set(evaluaciones_nc)
            
            # Serializar incluyendo datos completos
            serializer = self.get_serializer(matriz)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        # Procesar cada firma
        for field in ['firma_a', 'firma_b', 'firma_c', 'firma_d', 'firma_e']:
            if field in data and data[field].startswith('data:image'):
                # Convertir data URL a archivo
                format, imgstr = data[field].split(';base64,') 
                ext = format.split('/')[-1]
                
                file_name = f"{field}_{uuid.uuid4()}.{ext}"
                file_content = ContentFile(base64.b64decode(imgstr), name=file_name)
                data[field] = file_content
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
    
        file_fields = ['firma_a', 'firma_b', 'firma_c', 'firma_d', 'firma_e']
    
        for field in file_fields:
            if field in request.FILES:
                old_file = getattr(instance, field)
                if old_file:
                    old_file.delete(save=False)
                setattr(instance, field, request.FILES[field])
            elif field in data and data[field] == 'null':
                old_file = getattr(instance, field)
                if old_file:
                    old_file.delete(save=False)
                setattr(instance, field, None)
    
        # Elimina los campos de archivo para evitar problemas con el serializer
        for field in file_fields:
            data.pop(field, None)
    
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
    
        return Response(serializer.data)