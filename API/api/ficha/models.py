from django.db import models
# Por esta:
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()  # Esto usará el modelo definido en AUTH_USER_MODEL


class Institucion(models.Model):
    TIPO_CHOICES = [
        ('EESS', 'Establecimiento de Salud'),
        ('DIRIS', 'Dirección de Red Integrada de Salud'),
        ('DIRESA', 'Dirección Regional de Salud'),
        ('GERESA', 'Gerencia Regional de Salud'),
    ]
    
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    codigo = models.CharField(max_length=20, unique=True)
    categoria = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nombre}"

# Create your models here.
class Categoria(models.Model):
    name = models.CharField(max_length=500, verbose_name="Nombre")
    tipo = models.CharField(max_length=500, verbose_name="Tipo")

    def __str__(self):
        return f"{self.name} - {self.tipo}"
    
class Proceso(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='procesos')
    nombre = models.CharField(max_length=200)
    nombre_proceso = models.CharField(max_length=200)
    dueño_proceso = models.CharField(max_length=200)
    objetivo = models.TextField()
    objetivo_estrategico = models.TextField()
    prov_entrada = models.TextField()
    elemento_entrada = models.TextField()
    actividad_proceso = models.TextField()
    riesgos = models.TextField()
    registros = models.TextField()
    
    def __str__(self):
        return f"{self.categoria} - {self.nombre}"
    
class Subproceso(models.Model):
    NIVEL_CHOICES = [
        ('1', 'Nivel 1'),
        ('2', 'Nivel 2'),
        ('3', 'Nivel 3'),
    ]
    
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE, related_name='subprocesos')
    nivel = models.CharField(max_length=1, choices=NIVEL_CHOICES, default='1')
    nombre  = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['proceso']
    
    def __str__(self):
        return f"{self.proceso} - {self.nombre }"
    
class Verificador(models.Model):    
    subproceso = models.ForeignKey(Subproceso, on_delete=models.CASCADE, related_name='verificadores')
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Verificadores"
    
    def __str__(self):
        return f"{self.subproceso.nombre} - {self.descripcion[:50]}..."

