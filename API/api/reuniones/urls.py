from django.urls import path
from rest_framework.routers import DefaultRouter
from api.reuniones.views import *

router = DefaultRouter()

router.register(r'evento', EventoViewSet)
router.register(r'persona', PersonaViewSet)

urlpatterns = router.urls
