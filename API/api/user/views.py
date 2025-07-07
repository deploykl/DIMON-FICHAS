from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from api.user.serializers import *

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