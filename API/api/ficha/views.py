from datetime import datetime
import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
import requests
from django.db.models import Prefetch
from urllib.parse import urlencode
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from rest_framework.filters import OrderingFilter
from api.ficha.serializers import *
from django.core.exceptions import PermissionDenied

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
            
        ## Filtrar por usuario si no es superusuario
        #CONDICIONAL PARA VER TODOS LOS REGISTROS SOLO VEIA SI ES SUPERUSUARIO
        #if not self.request.user.is_superuser:
        #    queryset = queryset.filter(evaluacion__usuario=self.request.user)
        #    
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
            'descripcion_situacional': '',
            'semaforo': 'Verde' if evaluacion.estado == 'C' else 'Rojo',
            'riesgo_identificado': '',
            'medidas_correctivas': '',
            'hito_esperado': '',
            'responsable_directo': '',
            'plazo_inicio': hoy,
            'plazo_fin': hoy + timedelta(days=30),
            'funcionario_depen_directo': '',
            'funcionario_depen_indirecto': '',
            'firmas_adicionales': '',
        }
    
    def create(self, request, *args, **kwargs):
        """Endpoint para crear matriz con manejo de firmas en base64"""
        data = request.data.copy()
        
        # Procesar cada firma de base64 a archivo
        for field in ['firma_m','firma_a', 'firma_b', 'firma_c', 'firma_d', 'firma_e']:
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
        
        file_fields = ['firma_m', 'firma_a', 'firma_b', 'firma_c', 'firma_d', 'firma_e']
        
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
    

    def list(self, request, *args, **kwargs):
        # Debug: Verificar si hay matrices en la base de datos
        print(f"Total matrices en DB: {MatrizCompromiso.objects.count()}")
        
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class SeguimientoMatrizCompromisoViewSet(viewsets.ModelViewSet):
    queryset = SeguimientoMatrizCompromiso.objects.all()
    serializer_class = SeguimientoMatrizCompromisoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['matriz']
    ordering_fields = ['fecha_seguimiento', 'fecha_creacion']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        matriz_id = self.request.query_params.get('matriz_id')
        
        if matriz_id:
            queryset = queryset.filter(matriz_id=matriz_id)
            
        ## Filtrar por usuario si no es superusuario   SOLO ERA PARA SUPERUSUARIO
        #if not self.request.user.is_superuser:
        #    queryset = queryset.filter(matriz__evaluacion__usuario=self.request.user)
            
        return queryset.order_by('-fecha_seguimiento')
    
    def perform_create(self, serializer):
        # Asegúrate que matriz_id esté en los datos validados
        serializer.save(usuario_creacion=self.request.user)

        if 'matriz' not in serializer.validated_data:
            raise serializers.ValidationError({"matriz_id": "Este campo es requerido."})
        
        # Verificación de permisos
        matriz = serializer.validated_data['matriz']
        #if not self.request.user.is_superuser and matriz.evaluacion.usuario != self.request.user:
        #    raise PermissionDenied("No tienes permiso para crear seguimientos en esta matriz")
        
        serializer.save()
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Verifica permisos
        if not request.user.is_superuser and instance.matriz.evaluacion.usuario != request.user:
            return Response(
                {'error': 'No tienes permiso para editar este seguimiento'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
class AlertasViewSet(viewsets.ModelViewSet):
    serializer_class = AlertasSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["-fecha_creacion"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
    def get_queryset(self):
        #queryset = Alertas.objects.select_related('usuario').prefetch_related('seguimientos')
        #if not self.request.user.is_superuser:
        #    queryset = queryset.filter(usuario=self.request.user)
        #return queryset
        return Alertas.objects.select_related('usuario').prefetch_related('seguimientos').all()

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Verificar si el usuario actual es el creador de la alerta o es superusuario
        if instance.usuario != request.user and not request.user.is_superuser:
            return Response(
                {"detail": "No tienes permiso para eliminar esta alerta."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        return super().destroy(request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Verificar si el usuario actual es el creador de la alerta o es superusuario
        if instance.usuario != request.user and not request.user.is_superuser:
            return Response(
                {"detail": "No tienes permiso para editar esta alerta."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        # Para PATCH requests, usamos la misma verificación que para PUT
        return self.update(request, *args, **kwargs)


class SeguimientoAlertasViewSet(viewsets.ModelViewSet):
    queryset = SeguimientoAlertas.objects.all()
    serializer_class = SeguimientoAlertasSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['alerta']  # Usar 'alertas' en lugar de 'alerta'
    ordering_fields = ['fecha_seguimiento', 'fecha_creacion']

    def get_queryset(self):
        queryset = super().get_queryset()
        alerta_id = self.request.query_params.get('alerta')  # Usa 'alerta' aquí también
        if alerta_id:
            queryset = queryset.filter(alerta_id=alerta_id)  # Filtra por 'alerta_id'
        return queryset.order_by('-fecha_seguimiento')

    def perform_create(self, serializer):
        # Verificar que alertas está en los datos validados
        if 'alerta' not in serializer.validated_data:
            raise serializers.ValidationError({"alerta_id": "Este campo es requerido."})
            
        serializer.save(usuario_creacion=self.request.user)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Verifica permisos
        if not request.user.is_superuser and instance.alerta.usuario != request.user:
            return Response(
                {'error': 'No tienes permiso para editar este seguimiento'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    
class RenipressViewSet(ViewSet):
    permission_classes = [AllowAny]
    
    def list(self, request):
        codigo = request.query_params.get('COD_IPRESS')
        nombre = request.query_params.get('q')
        
        try:
            params = {
                'resource_id': '8bb014bd-bb39-40d8-bfd7-0c8bcb4eb37d',
                'limit': 10
            }
            
            if nombre:
                params['q'] = nombre
            elif codigo:
                # Formato CORRECTO para filtros en SUSALUD
                params['filters[COD_IPRESS]'] = codigo
            else:
                return Response({'error': 'Se requiere parámetro de búsqueda'}, status=400)
            
            # DEBUG: Verificar URL final
            final_url = f'http://datos.susalud.gob.pe/api/action/datastore/search.json?{urlencode(params)}'
            print("URL SUSALUD:", final_url)
            
            response = requests.get(
                'http://datos.susalud.gob.pe/api/action/datastore/search.json',
                params=params,
                timeout=5
            )
            response.raise_for_status()
            
            data = response.json()
            records = data.get('result', {}).get('records', [])
            
            # Filtrado adicional en caso de que la API no aplique bien el filtro
            if codigo:
                records = [r for r in records if str(r.get('COD_IPRESS')) == codigo]
            
            return Response({
                'success': True,
                'result': {
                    'records': records,
                    'total': len(records)
                }
            })
            
        except requests.RequestException as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)
            
