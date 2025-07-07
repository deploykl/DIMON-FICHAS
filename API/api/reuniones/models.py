from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Evento(models.Model):
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.descripcion} - {self.fecha}"

class Persona(models.Model):
    """Personas que pueden asistir a eventos"""
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

