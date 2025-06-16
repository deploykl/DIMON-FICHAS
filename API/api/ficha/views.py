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


    
class ProcesoViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = ProcesoSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
class SubprocesoViewSet(viewsets.ModelViewSet):
    queryset = Subproceso.objects.all()
    serializer_class = InstitucionSerializer
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
    