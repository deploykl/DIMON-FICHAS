from django.urls import path
from rest_framework.routers import DefaultRouter
from api.ficha.views import *

router = DefaultRouter()

router.register(r'categoria', CategoriaViewSet)
router.register(r'proceso', ProcesoViewSet)
router.register(r'subproceso', SubprocesoViewSet)
router.register(r'verificador', VerificadorViewSet)
router.register(r'evaluaciones', EvaluacionVerificadorViewSet)  # Añade esta línea
router.register(r'matriz-compromiso', MatrizCompromisoViewSet, basename='matriz-compromiso')


urlpatterns = router.urls
