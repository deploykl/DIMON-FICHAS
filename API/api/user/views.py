from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from api.user.serializers import *
import pandas as pd
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        # Devuelve solo los detalles del usuario autenticado
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    
class LoginView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación previa

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'detail': 'Las credenciales de autenticación no se proveyeron.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(username=username).first()

        if user is None:
            return Response(
                {'detail': 'Usuario no encontrado'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.check_password(password):
            return Response(
                {'detail': 'Contraseña incorrecta'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Verificar si el usuario está activo
        if not user.is_active:
            return Response(
                {'detail': 'Cuenta desactivada'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # Permitir acceso si es staff O superusuario
        if not user.is_staff and not user.is_superuser:
            return Response(
                {'detail': 'Su cuenta no tiene permisos de acceso al sistema'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)

        user_data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'access_ConsultaExterna': user.access_ConsultaExterna,
        }

        return Response(user_data, status=status.HTTP_200_OK)
            
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Crea un objeto RefreshToken a partir del token recibido
            token = RefreshToken(refresh_token)
            # Añade el token a la lista negra
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except InvalidToken:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'detail': 'El correo electrónico es requerido.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Si este correo existe en nuestro sistema, recibirás un enlace de recuperación.'}, 
                status=status.HTTP_200_OK  # No revelamos si el email existe o no
            )

        # Generar token
        reset_token = get_random_string(50)
        user.password_reset_token = reset_token
        user.password_reset_token_expires = timezone.now() + timedelta(hours=1)
        user.save()

        # En desarrollo, muestra el enlace en consola
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        print(f"\n--- Enlace de recuperación para {email}: {reset_link}\n")  # Para ver en consola

        # Enviar correo (en producción)
        send_mail(
            'Restablecer contraseña - Plataforma OBS Salud',
            f'''Hola {user.first_name or 'usuario'},

Para restablecer tu contraseña, haz clic en el siguiente enlace:
{reset_link}

Este enlace expirará en 1 hora.

Si no solicitaste este cambio, ignora este mensaje.

Atentamente,
Equipo de Plataforma OBS Salud
            ''',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response(
            {'detail': 'Si este correo existe en nuestro sistema, recibirás un enlace de recuperación.'}, 
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        password = request.data.get('password')
        password2 = request.data.get('password2')

        if not token or not password or not password2:
            return Response(
                {'detail': 'Todos los campos son requeridos.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if password != password2:
            return Response(
                {'detail': 'Las contraseñas no coinciden.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(
                password_reset_token=token,
                password_reset_token_expires__gt=timezone.now()
            )
        except User.DoesNotExist:
            return Response(
                {'detail': 'Token inválido o expirado.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(password)
        user.password_reset_token = None
        user.password_reset_token_expires = None
        user.save()

        return Response(
            {'detail': 'Contraseña restablecida correctamente.'}, 
            status=status.HTTP_200_OK
        )
        

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 50  # Puedes ajustar este valor
    page_size_query_param = 'page_size'
    max_page_size = 200
    
class ConsultaExternaViewSet(viewsets.ModelViewSet):
    queryset = ConsultaExterna.objects.all()
    serializer_class = ConsultaExternaSerializer
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = LargeResultsSetPagination

    @action(detail=False, methods=['post'], url_path='importar-excel')
    def importar_excel(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No se proporcionó archivo'}, status=status.HTTP_400_BAD_REQUEST)
    
        file = request.FILES['file']
        try:
            df = pd.read_excel(file)
            column_mapping = {
                0: 'tipo_seguro',
                1: 'fecha_nacimiento',
                2: 'sexo',
                3: 'lugar_procedencia',
                4: 'tipo_documento',
                5: 'documento',
                6: 'n_hcl',
                7: 'fecha_hora_cita_otorgada',
                8: 'fecha_hora_atencion',
                9: 'diagnostico_medico',
                10: 'dx_CIE_10_1',
                11: 'dx_CIE_10_2',
                12: 'dx_CIE_10_3',
                13: 'especialidad'
            }
            
            if len(df.columns) < len(column_mapping):
                return Response(
                    {'error': f'El archivo Excel debe tener al menos {len(column_mapping)} columnas'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            created_count = 0
            updated_count = 0
            errors = []
            fechas_omitidas = 0
            fecha_limite = datetime(2025, 3, 1).date()
            
            for index, row in df.iterrows():
                try:
                    data = {}
                    for col_index, field_name in column_mapping.items():
                        if col_index < len(row):
                            data[field_name] = row[col_index] if not pd.isna(row[col_index]) else None
                    
                    # Validar campos requeridos
                    required_fields = ['tipo_seguro', 'documento', 'fecha_hora_cita_otorgada', 'fecha_hora_atencion']
                    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
                    
                    if missing_fields:
                        errors.append(f"Fila {index + 2}: Faltan campos requeridos: {', '.join(missing_fields)}")
                        continue
                    
                    # Convertir y validar fechas
                    try:
                        fecha_cita = pd.to_datetime(data['fecha_hora_cita_otorgada'])
                        fecha_atencion = pd.to_datetime(data['fecha_hora_atencion'])
                        
                        # Omitir registros con fechas anteriores
                        if fecha_cita.date() < fecha_limite or fecha_atencion.date() < fecha_limite:
                            fechas_omitidas += 1
                            errors.append(
                                f"Fila {index + 2}: Omitida - Fecha cita: {fecha_cita.date()}, "
                                f"Fecha atención: {fecha_atencion.date()}"
                            )
                            continue
                        
                        data['fecha_hora_cita_otorgada'] = fecha_cita
                        data['fecha_hora_atencion'] = fecha_atencion
                    except Exception as e:
                        errors.append(f"Fila {index + 2}: Error en formato de fecha - {str(e)}")
                        continue
                    
                    # Procesar el resto de campos
                    if 'fecha_nacimiento' in data and data['fecha_nacimiento']:
                        try:
                            data['fecha_nacimiento'] = pd.to_datetime(data['fecha_nacimiento']).date()
                        except:
                            data['fecha_nacimiento'] = None
                    
                    if 'sexo' in data and data['sexo']:
                        data['sexo'] = str(data['sexo']).strip().upper()[:1]
                    
                    for cie_field in ['dx_CIE_10_1', 'dx_CIE_10_2', 'dx_CIE_10_3']:
                        if cie_field in data and data[cie_field]:
                            data[cie_field] = str(data[cie_field]).strip()
                    
                    # Crear o actualizar registro
                    consulta, created = ConsultaExterna.objects.update_or_create(
                        documento=data['documento'],
                        fecha_hora_cita_otorgada=data['fecha_hora_cita_otorgada'],
                        defaults={
                            **data,
                            'creado_por': request.user
                        }
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                        
                except Exception as e:
                    errors.append(f"Fila {index + 2}: Error - {str(e)}")
                    continue
                
            # Mensaje resumen
            message = 'Importación completada'
            if fechas_omitidas > 0:
                message = f'Importación completada (omitidas {fechas_omitidas} filas con fechas anteriores a marzo 2025)'
            
            return Response({
                'success': True,
                'message': message,
                'total_filas': len(df),
                'creados': created_count,
                'actualizados': updated_count,
                'omitidas': fechas_omitidas,
                'errores': len(errors),
                'detalle_errores': errors[:20]  # Mostrar más errores si hay fechas omitidas
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': f"Error al procesar el archivo: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )