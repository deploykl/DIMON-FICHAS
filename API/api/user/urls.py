from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from api.user.views import *

router = DefaultRouter()
router.register(r'consultas-externas', ConsultaExternaViewSet, basename='consulta-externa')
router.register(r'cirugias', CirugiaViewSet, basename='cirugias')


urlpatterns = [  
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    #path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
] + router.urls


