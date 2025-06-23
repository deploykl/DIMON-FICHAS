from datetime import datetime
import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
import requests
from django.db.models import Prefetch

from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework import viewsets, status, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from rest_framework.filters import OrderingFilter, SearchFilter
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
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    serializer_class = MatrizCompromisoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['evaluacion']
    ordering_fields = '__all__'
    
    def get_queryset(self):
        queryset = MatrizCompromiso.objects.all().select_related(
            'evaluacion__usuario',
            'evaluacion__verificador__subproceso__proceso'
        ).prefetch_related(
            Prefetch(
                'evaluaciones_nc',
                queryset=EvaluacionVerificador.objects.select_related(
                    'verificador__subproceso__proceso',
                    'usuario'
                )
            )
        )
        
        # Filtrar por evaluación si se especifica
        evaluacion_id = self.request.query_params.get('evaluacion_id')
        if evaluacion_id:
            queryset = queryset.filter(evaluacion_id=evaluacion_id)
            
        # Filtrar por usuario si no es superusuario
        if not self.request.user.is_superuser:
            queryset = queryset.filter(evaluacion__usuario=self.request.user)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def por_evaluacion(self, request):
        """Endpoint para obtener o crear matriz por evaluación"""
        evaluacion_id = request.query_params.get('evaluacion_id')
        if not evaluacion_id:
            return Response(
                {'error': 'Se requiere el parámetro evaluacion_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            evaluacion = EvaluacionVerificador.objects.get(id=evaluacion_id)
            
            # Verificar permisos - solo el usuario creador o superusuario puede acceder
            if not request.user.is_superuser and evaluacion.usuario != request.user:
                return Response(
                    {'error': 'No tienes permiso para acceder a esta evaluación'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            matriz, created = MatrizCompromiso.objects.get_or_create(
                evaluacion=evaluacion,
                defaults=self._get_default_matriz_data(evaluacion)
            )
            
            # Si ya existía, actualizar con evaluaciones NC relacionadas
            if not created:
                nc_evaluaciones = EvaluacionVerificador.objects.filter(
                    verificador__subproceso=evaluacion.verificador.subproceso,
                    estado='NC'
                )
                matriz.evaluaciones_nc.set(nc_evaluaciones)
                matriz.save()
            
            serializer = self.get_serializer(matriz)
            return Response(serializer.data)
            
        except EvaluacionVerificador.DoesNotExist:
            return Response(
                {'error': 'Evaluación no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
            
    @action(detail=False, methods=['post'])
    def generar_completa(self, request):
        """Endpoint para generar matriz completa con múltiples evaluaciones"""
        evaluaciones_ids = request.data.get('evaluaciones_ids', [])
        
        if not evaluaciones_ids:
            return Response(
                {'error': 'Se requiere al menos una evaluación'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            evaluaciones = EvaluacionVerificador.objects.filter(
                id__in=evaluaciones_ids
            ).select_related(
                'verificador__subproceso__proceso',
                'usuario'
            )
            
            # Verificar que todas las evaluaciones existen
            if len(evaluaciones) != len(evaluaciones_ids):
                missing_ids = set(evaluaciones_ids) - set(evaluaciones.values_list('id', flat=True))
                return Response(
                    {'error': f'Evaluaciones no encontradas: {missing_ids}'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Verificar permisos para todas las evaluaciones
            if not request.user.is_superuser:
                for eval in evaluaciones:
                    if eval.usuario != request.user:
                        return Response(
                            {'error': 'No tienes permiso para algunas evaluaciones'},
                            status=status.HTTP_403_FORBIDDEN
                        )
            
            primera_eval = evaluaciones.first()
            
            # Crear matriz con valores por defecto
            matriz = MatrizCompromiso.objects.create(
                evaluacion=primera_eval,
                **self._get_default_matriz_data(primera_eval)
            )
            
            # Asociar evaluaciones a la matriz
            matriz.evaluaciones_nc.set(evaluaciones)
            
            # Serializar con todos los datos
            serializer = self.get_serializer(matriz)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Error al generar matriz: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _get_default_matriz_data(self, evaluacion):
        """Método helper para obtener datos por defecto para una nueva matriz"""
        hoy = datetime.now().date()
        return {
            'descripcion_situacional': 'Descripción pendiente',
            'semaforo': 'Verde' if evaluacion.estado == 'C' else 'Rojo',
            'riesgo_identificado': 'Riesgos pendientes de identificación',
            'medidas_correctivas': 'Medidas correctivas pendientes',
            'hito_esperado': 'Hito esperado pendiente',
            'responsable_directo': 'Por definir',
            'plazo_inicio': hoy,
            'plazo_fin': hoy + timedelta(days=30),
            'funcionario_depen_directo': 'Por definir',
            'funcionario_depen_indirecto': 'Por definir',
            'firmas_adicionales': '',
        }
    
    def create(self, request, *args, **kwargs):
        """Endpoint para crear matriz con manejo de firmas en base64"""
        data = request.data.copy()
        
        # Procesar cada firma de base64 a archivo
        for field in ['firma_a', 'firma_b', 'firma_c', 'firma_d', 'firma_e']:
            if field in data and isinstance(data[field], str) and data[field].startswith('data:image'):
                try:
                    format, imgstr = data[field].split(';base64,') 
                    ext = format.split('/')[-1]
                    file_name = f"{field}_{uuid.uuid4()}.{ext}"
                    file_content = ContentFile(base64.b64decode(imgstr), name=file_name)
                    data[field] = file_content
                except Exception as e:
                    return Response(
                        {'error': f'Error procesando {field}: {str(e)}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        # Asignar usuario si no es superusuario
        if not request.user.is_superuser:
            evaluacion_id = data.get('evaluacion')
            if evaluacion_id:
                evaluacion = EvaluacionVerificador.objects.filter(id=evaluacion_id).first()
                if evaluacion and evaluacion.usuario != request.user:
                    return Response(
                        {'error': 'No tienes permiso para crear matriz para esta evaluación'},
                        status=status.HTTP_403_FORBIDDEN
                    )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """Endpoint para actualizar matriz con manejo de firmas"""
        instance = self.get_object()
        data = request.data.copy()
        
        # Verificar permisos
        if not request.user.is_superuser and instance.evaluacion.usuario != request.user:
            return Response(
                {'error': 'No tienes permiso para editar esta matriz'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        file_fields = ['firma_a', 'firma_b', 'firma_c', 'firma_d', 'firma_e']
        
        # Manejar actualización/eliminación de firmas
        for field in file_fields:
            if field in request.FILES:
                # Eliminar archivo antiguo si existe
                old_file = getattr(instance, field)
                if old_file:
                    old_file.delete(save=False)
                setattr(instance, field, request.FILES[field])
            elif field in data and data[field] == 'null':
                # Eliminar firma existente
                old_file = getattr(instance, field)
                if old_file:
                    old_file.delete(save=False)
                setattr(instance, field, None)
                data.pop(field)
            elif field in data and isinstance(data[field], str) and data[field].startswith('data:image'):
                # Convertir base64 a archivo
                try:
                    format, imgstr = data[field].split(';base64,') 
                    ext = format.split('/')[-1]
                    file_name = f"{field}_{uuid.uuid4()}.{ext}"
                    file_content = ContentFile(base64.b64decode(imgstr), name=file_name)
                    setattr(instance, field, file_content)
                    data.pop(field)
                except Exception as e:
                    return Response(
                        {'error': f'Error procesando {field}: {str(e)}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
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
    

    def list(self, request, *args, **kwargs):
        # Debug: Verificar si hay matrices en la base de datos
        print(f"Total matrices en DB: {MatrizCompromiso.objects.count()}")
        
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            print(f"Datos enviados: {serializer.data}")  # Debug
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        print(f"Datos enviados (no paginados): {serializer.data}")  # Debug
        return Response(serializer.data)
    
# Nuevo ViewSet para el proxy de SUSALUD
class RenipressViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['q']  # Campo para la búsqueda

    def list(self, request, *args, **kwargs):
        search_term = request.query_params.get('q', '')
        
        try:
            response = requests.get(
                'http://datos.susalud.gob.pe/api/action/datastore/search.json',
                params={
                    'resource_id': '8bb014bd-bb39-40d8-bfd7-0c8bcb4eb37d',
                    'q': search_term,
                    'limit': 10
                },
                timeout=5
            )
            response.raise_for_status()
            return Response(response.json())
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=500)