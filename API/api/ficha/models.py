from time import timezone
from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()  # Esto usará el modelo definido en AUTH_USER_MODEL
from datetime import timedelta  # Añadir esto al inicio del archivo models.py

# Create your models here.
class Categoria(models.Model):
    name = models.CharField(max_length=500, verbose_name="Nombre")
    tipo = models.CharField(max_length=500, verbose_name="Tipo")

    def __str__(self):
        return f"{self.name} - {self.tipo}"
    
class Proceso(models.Model):
    titulo = models.TextField()
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

class EvaluacionVerificador(models.Model):
    ESTADO_CHOICES = [
        ('C', 'Cumple'),
        ('NC', 'No Cumple'),
        ('NA', 'No Aplica'),
    ]
    TIPO_CHOICES = [
        ('EESS', 'Establecimiento de Salud'),
        ('DIRIS', 'Dirección de Red Integrada de Salud'),
        ('DIRESA', 'Dirección Regional de Salud'),
        ('GERESA', 'Gerencia Regional de Salud'),
    ]   
 # Campos del verificador
    verificador = models.ForeignKey('Verificador', on_delete=models.CASCADE, related_name='evaluaciones')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    
    # Campos de la IPRESS (se capturan en la evaluación)
    establecimiento = models.CharField(max_length=200, verbose_name="Nombre de la IPRESS")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo de IPRESS")
    codigo = models.CharField(max_length=20, verbose_name="Código de la IPRESS")
    categoria = models.CharField(max_length=100, verbose_name="Categoría")
    departamento = models.CharField(max_length=100, verbose_name="Departamento", blank=True, null=True)
    provincia = models.CharField(max_length=100, verbose_name="Provincia", blank=True, null=True)
    distrito = models.CharField(max_length=100, verbose_name="Distrito", blank=True, null=True)
    disa = models.CharField(max_length=100, verbose_name="DISA", blank=True, null=True)
    institucion = models.CharField(max_length=100, verbose_name="Institucion", blank=True, null=True)

    class Meta:
        ordering = ['-fecha_evaluacion']
        verbose_name_plural = "Evaluaciones"

    def __str__(self):
        return f"{self.verificador} - {self.establecimiento} ({self.get_estado_display()})"
    
#MATRIZ DE COMPROMISO
class MatrizCompromiso(models.Model):
    evaluacion = models.ForeignKey(EvaluacionVerificador, on_delete=models.CASCADE, related_name='matrices')
    descripcion_situacional = models.TextField(verbose_name="Descripción del estado situacional")
    semaforo = models.CharField(max_length=50, verbose_name="Semáforo")
    riesgo_identificado = models.TextField(verbose_name="Identificación del Riesgo")
    medidas_correctivas = models.TextField(verbose_name="Medidas correctivas/Compromisos")
    hito_esperado = models.TextField(verbose_name="Hito esperado")
    plazo_inicio = models.DateField()
    plazo_fin = models.DateField()
    responsable_directo = models.CharField(max_length=200, verbose_name="Responsable directo (A)")
    funcionario_depen_directo = models.CharField(max_length=200, verbose_name="Funcionario (B)")
    funcionario_depen_indirecto = models.CharField(max_length=200, verbose_name="Funcionario (C)")
    funcionario_d = models.CharField(max_length=200, blank=True, null=True,verbose_name="Funcionario (D)")
    funcionario_e = models.CharField(max_length=200, blank=True, null=True, verbose_name="Funcionario (E)")
    firmas_adicionales = models.TextField(verbose_name="Firmas adicionales (máx. 5)", blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
     # Relación ManyToMany para agrupar evaluaciones NC relacionadas
    evaluaciones_nc = models.ManyToManyField(
        EvaluacionVerificador,
        related_name='matrices_asociadas',
        verbose_name="Evaluaciones No Conformes"
    )
    # Campos para almacenar las firmas como imágenes
    firma_m = models.ImageField(
        upload_to='firmas_matrices/',
        verbose_name="Firma Monitor  (M)",
        null=True,
        blank=True
    )
    firma_a = models.ImageField(
        upload_to='firmas_matrices/',
        verbose_name="Firma Responsable Directo (A)",
        null=True,
        blank=True
    )
    firma_b = models.ImageField(
        upload_to='firmas_matrices/',
        verbose_name="Firma Funcionario (B)",
        null=True,
        blank=True
    )
    firma_c = models.ImageField(
        upload_to='firmas_matrices/',
        verbose_name="Firma Funcionario (C)",
        null=True,
        blank=True
    )
    firma_d = models.ImageField(
        upload_to='firmas_matrices/',
        verbose_name="Firma Funcionario (D)",
        null=True,
        blank=True
    )
    firma_e = models.ImageField(
        upload_to='firmas_matrices/',
        verbose_name="Firma Funcionario (E)",
        null=True,
        blank=True
    )
    ultima_alerta_enviada = models.DateField(null=True, blank=True)
    proxima_alerta = models.DateField(null=True, blank=True)
    alertas_enviadas = models.PositiveIntegerField(default=0)
    
    def calcular_proxima_alerta(self):
        hoy = timezone.now().date()
        dias_restantes = (self.plazo_fin - hoy).days
        
        if dias_restantes <= 0:
            return None  # Plazo vencido, no más alertas
        
        if dias_restantes <= 3:
            return hoy + timedelta(days=1)  # Alerta diaria
        elif dias_restantes <= 7:
            return hoy + timedelta(days=3)  # Cada 3 días
        else:
            return hoy + timedelta(days=7)  # Semanal

    class Meta:
        verbose_name = "Matriz de Compromiso"
        verbose_name_plural = "Matrices de Compromiso"

    def __str__(self):
        return f"Matriz para {self.evaluacion.establecimiento} ({self.evaluacion.codigo})"
    
    # Propiedad para acceder fácilmente a los datos de la IPRESS
    @property
    def datos_ipress(self):
        return {
            'establecimiento': self.evaluacion.establecimiento,
            'codigo': self.evaluacion.codigo,
            'tipo': self.evaluacion.get_tipo_display(),
            'categoria': self.evaluacion.categoria
        }
        
class SeguimientoMatrizCompromiso(models.Model):
    ESTADO_SEGUIMIENTO_CHOICES = [
        ('P', 'Pendiente'),
        ('EP', 'En Progreso'),
        ('C', 'Completado'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
    ]
    # Relación con la matriz original (con acceso a todos sus campos)
    matriz = models.ForeignKey(MatrizCompromiso, on_delete=models.CASCADE, related_name='seguimientos')
        
    # Campos específicos del seguimiento
    fecha_seguimiento = models.DateField(verbose_name="Fecha de seguimiento")
    estado = models.CharField(max_length=2, choices=ESTADO_SEGUIMIENTO_CHOICES, default='P',verbose_name="Estado del seguimiento")
    analisis_accion = models.TextField(verbose_name="Análisis/Acción realizada")
    
    # Fechas de registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    # Agrega esta relación
    usuario_creacion = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='seguimientos_creados',
        verbose_name="Usuario que registró"
    )
    class Meta:
        verbose_name = "Seguimiento de Matriz de Compromiso"
        verbose_name_plural = "Seguimientos de Matrices de Compromiso"
        ordering = ['-fecha_seguimiento', 'matriz']

    def __str__(self):
        return f"Seguimiento {self.get_estado_display()} para {self.matriz.evaluacion.establecimiento} ({self.fecha_seguimiento})"
    
    # Propiedades para acceder a los datos relacionados sin duplicarlos
    @property
    def datos_ipress(self):
        """Accede a los datos de IPRESS a través de la relación con EvaluacionVerificador"""
        return {
            'establecimiento': self.matriz.evaluacion.establecimiento,
            'codigo': self.matriz.evaluacion.codigo,
            'tipo': self.matriz.evaluacion.get_tipo_display(),
            'categoria': self.matriz.evaluacion.categoria,
            'departamento': self.matriz.evaluacion.departamento,
            'provincia': self.matriz.evaluacion.provincia,
            'distrito': self.matriz.evaluacion.distrito
        }
    
    @property
    def compromisos_originales(self):
        """Accede a los datos de compromisos de la matriz original"""
        return {
            'medidas_correctivas': self.matriz.medidas_correctivas,
            'hito_esperado': self.matriz.hito_esperado,
            'plazo_inicio': self.matriz.plazo_inicio,
            'plazo_fin': self.matriz.plazo_fin,
            'responsable': self.matriz.responsable_directo
        }
        
# Create your models here.
class Alertas(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    codigo = models.CharField(
        max_length=50, 
        verbose_name="Código", 
        unique=True,
        editable=False,  # No se puede editar manualmente
        default=uuid.uuid4  # Genera un UUID por defecto
    )    
    tipo = models.CharField(max_length=500, verbose_name="Tipo")
    descripcion = models.CharField(max_length=500, verbose_name="Descripción")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Si es un nuevo registro y no tiene código asignado
        if not self.codigo:
            self.codigo = f"ALERT-{uuid.uuid4().hex[:8].upper()}"  # Formato más legible
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario} - {self.tipo} - {self.codigo}"
    
    
# Create your models here.
class SeguimientoAlertas(models.Model):
    # Campos específicos del seguimiento
    fecha_seguimiento = models.DateField(verbose_name="Fecha de seguimiento")
    estado = models.TextField(verbose_name="Estado")
    analisis_accion = models.TextField(verbose_name="Análisis/Acción realizada")
    alerta = models.ForeignKey(Alertas, on_delete=models.CASCADE, related_name='seguimientos')

    # Fechas de registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    # Agrega esta relación
    usuario_creacion = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='seguimientos_alertas_creados',
        verbose_name="Usuario que registró"
    )
    def __str__(self):
        return f"{self.fecha_seguimiento} - {self.usuario_creacion}"

