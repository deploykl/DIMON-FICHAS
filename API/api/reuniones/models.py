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
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    # Campos de la IPRESS (se capturan en la evaluación)
    establecimiento = models.CharField(max_length=200, verbose_name="Nombre de la IPRESS", blank=True, null=True)
    codigo = models.CharField(max_length=20, verbose_name="Código de la IPRESS", blank=True, null=True)
    categoria = models.CharField(max_length=100, verbose_name="Categoría", blank=True, null=True)
    departamento = models.CharField(max_length=100, verbose_name="Departamento", blank=True, null=True)
    provincia = models.CharField(max_length=100, verbose_name="Provincia", blank=True, null=True)
    distrito = models.CharField(max_length=100, verbose_name="Distrito", blank=True, null=True)
    disa = models.CharField(max_length=100, verbose_name="DISA", blank=True, null=True)
    institucion = models.CharField(max_length=100, verbose_name="Institucion", blank=True, null=True)    
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

