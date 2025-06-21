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
                    'semaforo': 'Verde' if evaluacion.estado == 'C' else 'Rojo',
                    'riesgo_identificado': 'Cumple con observaciones' if evaluacion.estado == 'C' else 'Riesgos identificados',
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
            # Obtener todas las evaluaciones sin filtrar por estado
            evaluaciones = EvaluacionVerificador.objects.filter(
                id__in=evaluaciones_ids
            ).select_related(
                'verificador__subproceso__proceso',
                'usuario'
            )
            
            if not evaluaciones.exists():
                return Response(
                    {'error': 'No se encontraron evaluaciones para generar la matriz'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Obtener la evaluación principal (primera de la lista)
            primera_eval = evaluaciones.first()
            
            # Fechas por defecto (hoy y 30 días después)
            hoy = datetime.now().date()
            plazo_fin = hoy + timedelta(days=30)
            
            # Crear matriz con valores por defecto
            matriz = MatrizCompromiso.objects.create(
                evaluacion=primera_eval,
                descripcion_situacional='Descripción pendiente',
                semaforo='Verde' if not evaluaciones.filter(estado='NC').exists() else 'Rojo',
                riesgo_identificado='Riesgos pendientes de identificación',
                medidas_correctivas='Medidas correctivas pendientes',
                hito_esperado='Hito esperado pendiente',
                responsable_directo='Por definir',
                plazo_inicio=hoy,  # Fecha actual como valor por defecto
                plazo_fin=plazo_fin,  # 30 días después como valor por defecto
                funcionario_depen_directo='Por definir',
                funcionario_depen_indirecto='Por definir',
                firmas_adicionales='',
                firma_a=None,
                firma_b=None,
                firma_c=None,
                firma_d=None,
                firma_e=None,
                funcionario_d='',
                funcionario_e=''
            )
            
            # Asociar TODAS las evaluaciones a la matriz
            matriz.evaluaciones_nc.set(evaluaciones)
            
            # Serializar incluyendo datos completos
            serializer = self.get_serializer(matriz)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Error al generar matriz: {str(e)}'},
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