from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import datetime
from api.Choises import GENDER_CHOICES 

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d',default='img/empty.png', null = True, blank = True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Género", null=True, blank=True)
    password_reset_token = models.CharField(max_length=50, null=True, blank=True)
    password_reset_token_expires = models.DateTimeField(null=True, blank=True)
    telegram_chat_id = models.BigIntegerField(verbose_name="ID de Chat de Telegram",null=True,blank=True, unique=True,)
    
    access_ConsultaExterna = models.BooleanField(default=False)
    codigo = models.CharField(null=True, blank=True,max_length=8)
    nombre = models.CharField(null=True, blank=True,max_length=200)
    distrito = models.CharField(null=True, blank=True,max_length=100)
    disa = models.CharField(null=True, blank=True,max_length=100)
    categoria = models.CharField(null=True, blank=True,max_length=20)
    
    def delete(self, *args, **kwargs):
        try:
            super().delete(*args, **kwargs)
        except IntegrityError as e:
            print(f"Error al eliminar usuario: {e}")
            # Puedes lanzar la excepción de nuevo si quieres manejarla en otra parte
            raise
        
    def has_perm(self, perm, obj=None):
        """Solo los superusuarios pueden acceder al admin de Django."""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Solo los superusuarios pueden ver el módulo 'admin'."""
        return self.is_superuser
    
# Create your models here.
class Directorio(models.Model):
    name = models.CharField(max_length=500, verbose_name="Nombre")
    tipo = models.CharField(max_length=500, verbose_name="Tipo")

    def __str__(self):
        return f"{self.name} - {self.tipo}"
    
class ConsultaExterna(models.Model):
    
    tipo_seguro = models.CharField(max_length=70)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=GENDER_CHOICES)
    lugar_procedencia = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=50)
    documento = models.CharField(max_length=20)
    n_hcl = models.CharField(max_length=20, verbose_name="Número de Historia Clínica")
    fecha_hora_cita_otorgada = models.DateTimeField()
    fecha_hora_atencion = models.DateTimeField()
    diagnostico_medico = models.TextField()
    dx_CIE_10_1 = models.CharField(max_length=10, verbose_name="Diagnóstico CIE-10 Principal")
    dx_CIE_10_2 = models.CharField(max_length=10, verbose_name="Diagnóstico CIE-10 Secundario", blank=True, null=True)
    dx_CIE_10_3 = models.CharField(max_length=10, verbose_name="Diagnóstico CIE-10 Terciario", blank=True, null=True)
    especialidad = models.CharField(max_length=100)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='consultas_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consulta {self.id} - {self.documento} - {self.fecha_hora_atencion.date()}"

    def clean(self):
        fecha_limite = datetime(2025, 3, 1).date()
        
        if self.fecha_hora_cita_otorgada.date() < fecha_limite:
            raise ValidationError('La fecha de cita debe ser a partir del 1 de marzo de 2025')
            
        if self.fecha_hora_atencion.date() < fecha_limite:
            raise ValidationError('La fecha de atención debe ser a partir del 1 de marzo de 2025')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)