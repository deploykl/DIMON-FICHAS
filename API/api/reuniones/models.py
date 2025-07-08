from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Evento(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROGRESO', 'En Progreso'),
        ('FINALIZADO', 'Finalizado'),
    ]
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE'
    )    
    def __str__(self):
        return f"{self.descripcion} - {self.fecha} ({self.estado})"

    def actualizar_estado(self):
        ahora = timezone.now()
        fecha_hora_inicio = timezone.make_aware(
            timezone.datetime.combine(self.fecha, self.hora_inicio))
        fecha_hora_fin = timezone.make_aware(
            timezone.datetime.combine(self.fecha, self.hora_fin))
        
        nuevo_estado = self.estado
        
        if ahora > fecha_hora_fin:
            nuevo_estado = 'FINALIZADO'
        elif ahora >= fecha_hora_inicio:
            nuevo_estado = 'EN_PROGRESO'
        else:
            nuevo_estado = 'PENDIENTE'
            
        if self.estado != nuevo_estado:
            self.estado = nuevo_estado
            self.save(update_fields=['estado'])
        
        return self.estado

    def save(self, *args, **kwargs):
        # Actualizar el estado antes de guardar
        self.actualizar_estado()
        super().save(*args, **kwargs)
        
class Persona(models.Model):
    eventos = models.ManyToManyField(Evento, blank=True, related_name='participantes')  # <--- Añade esta línea
    dni = models.CharField(max_length=50, verbose_name="DNI", unique=False)    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
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
    firma= models.ImageField(
        upload_to='reuniones/',
        verbose_name="Firma",
        null=True,
        blank=True
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

