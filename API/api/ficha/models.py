from time import timezone
from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import requests
User = get_user_model()  # Esto usará el modelo definido en AUTH_USER_MODEL
from datetime import timedelta, datetime
from django.utils import timezone

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
 # Agrega estos nuevos campos
    hora_envio = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Hora de envío programada",
        help_text="Hora a la que se enviarán los recordatorios"
    )
    
    def save(self, *args, **kwargs):
        # Si es un nuevo registro y no tiene código asignado
        if not self.codigo:
            self.codigo = f"ALERT-{uuid.uuid4().hex[:8].upper()}"  # Formato más legible
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario} - {self.tipo} - {self.codigo}"
    
    
# Create your models here.
class SeguimientoAlertas(models.Model):
    # Opciones de frecuencia de envío
    FRECUENCIA_CHOICES = [
        ('hoy', 'Hoy mismo'),
        ('diario', 'Diario'),
        ('2dias', 'Cada 2 días'),
        ('3dias', 'Cada 3 días'),
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
        ('personalizado', 'Personalizado'),
    ]
    
    # Opciones de estado del seguimiento
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('EP', 'En Progreso'),
        ('C', 'Completado'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
    ]
    
    # Campos específicos del seguimiento
    fecha_seguimiento = models.DateTimeField(
        verbose_name="Fecha y hora de seguimiento",
        help_text="Fecha y hora en que se realizó el seguimiento"
    )
    estado = models.CharField(
        max_length=2,
        choices=ESTADO_CHOICES,
        default='P',
        verbose_name="Estado del seguimiento"
    )
    analisis_accion = models.TextField(
        verbose_name="Análisis/Acción realizada",
        help_text="Descripción detallada del análisis y acciones tomadas"
    )
    alerta = models.ForeignKey(
        'Alertas',
        on_delete=models.CASCADE,
        related_name='seguimientos',
        verbose_name="Alerta relacionada"
    )
    
    # Campos para programación de envíos
    frecuencia_envio = models.CharField(
        max_length=20, 
        choices=FRECUENCIA_CHOICES, 
        null=True, 
        blank=True,
        verbose_name="Frecuencia de recordatorio",
        help_text="Frecuencia con la que se enviarán recordatorios"
    )
    hora_envio = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Hora de envío programada",
        help_text="Hora específica para enviar los recordatorios (formato HH:MM)"
    )
    dias_personalizados = models.PositiveIntegerField(
        null=True, 
        blank=True,
        verbose_name="Días para recordatorio personalizado",
        help_text="Número de días para recordatorios personalizados"
    )
    proximo_envio = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Próximo envío programado",
        help_text="Fecha y hora del próximo recordatorio automático"
    )
    enviar_notificacion = models.BooleanField(
        default=True,
        verbose_name="Enviar notificación",
        help_text="Activar para enviar notificaciones automáticas"
    )
    enviar_ahora = models.BooleanField(
        default=False,
        verbose_name="Enviar notificación inmediata",
        help_text="Marcar para enviar notificación inmediatamente al guardar"
    )
    
    # Fechas de registro
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de última actualización"
    )
    
    # Relación con usuario
    usuario_creacion = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='seguimientos_alertas_creados',
        verbose_name="Usuario que registró"
    )

    class Meta:
        verbose_name = "Seguimiento de Alerta"
        verbose_name_plural = "Seguimientos de Alertas"
        ordering = ['-fecha_seguimiento']
        indexes = [
            models.Index(fields=['proximo_envio']),
            models.Index(fields=['alerta']),
            models.Index(fields=['usuario_creacion']),
        ]

    def __str__(self):
        return f"Seguimiento #{self.id} - Alerta {self.alerta.codigo} - {self.get_estado_display()}"

    def calcular_proximo_envio(self):
        if not self.frecuencia_envio or not self.hora_envio:
            return None
            
        fecha_actual = timezone.now().date()
        hora_envio = self.hora_envio
        
        # Calcula la fecha base según la frecuencia
        if self.frecuencia_envio == 'diario':
            next_date = fecha_actual + timedelta(days=1)
        elif self.frecuencia_envio == '2dias':
            next_date = fecha_actual + timedelta(days=2)
        elif self.frecuencia_envio == '3dias':
            next_date = fecha_actual + timedelta(days=3)
        elif self.frecuencia_envio == 'semanal':
            next_date = fecha_actual + timedelta(weeks=1)
        elif self.frecuencia_envio == 'mensual':
            next_date = fecha_actual + timedelta(days=30)
        elif self.frecuencia_envio == 'personalizado' and self.dias_personalizados:
            next_date = fecha_actual + timedelta(days=self.dias_personalizados)
        else:
            return None
            
        # Combina la nueva fecha con la hora programada
        return datetime.combine(next_date, hora_envio)
    
    def enviar_notificaciones(self):
        if not self.enviar_notificacion:
            return
            
        # Enviar correo electrónico
        self.enviar_correo()
        
        # Enviar mensaje a Telegram
        self.enviar_telegram()
    
    def enviar_correo(self):
        asunto = f"[Seguimiento] Alerta {self.alerta.codigo} - {self.get_estado_display()}"
        
        mensaje = f"""
        Detalles del seguimiento:
        
        Alerta: {self.alerta.codigo} - {self.alerta.tipo}
        Estado: {self.get_estado_display()}
        Fecha seguimiento: {self.fecha_seguimiento.strftime('%d/%m/%Y %H:%M')}
        
        Análisis/Acción realizada:
        {self.analisis_accion}
        
        Registrado por: {self.usuario_creacion.get_full_name() if self.usuario_creacion else 'Sistema'}
        Fecha registro: {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}
        """
        
        if self.proximo_envio:
            mensaje += f"\nPróximo recordatorio: {self.proximo_envio.strftime('%d/%m/%Y %H:%M')}"
        
        try:
            destinatarios = [self.usuario_creacion.email] if self.usuario_creacion else []
            
            # Agregar destinatarios adicionales si están configurados
            if hasattr(settings, 'ALERTAS_EMAIL_CC'):
                destinatarios += settings.ALERTAS_EMAIL_CC
                
            send_mail(
                asunto,
                mensaje.strip(),
                settings.EMAIL_FROM,
                destinatarios,
                fail_silently=False,
            )
        except Exception as e:
            # Registrar el error en logs
            from django.core import mail
            mail.mail_admins(
                subject=f"Error enviando notificación de seguimiento {self.id}",
                message=f"Error: {str(e)}"
            )
    
    def enviar_telegram(self):
        estado_emoji = {
            'P': '⏳',
            'EP': '🔄',
            'C': '✅',
            'A': '👍',
            'R': '👎'
        }.get(self.estado, 'ℹ️')
        
        mensaje = f"""
        {estado_emoji} *Seguimiento de Alerta* {estado_emoji}
        
        *Alerta*: {self.alerta.codigo} - {self.alerta.tipo}
        *Estado*: {self.get_estado_display()}
        *Fecha*: {self.fecha_seguimiento.strftime('%d/%m/%Y %H:%M')}
        
        *Acción*: 
        {self.analisis_accion[:200]}...
        
        *Usuario*: {self.usuario_creacion.get_full_name() if self.usuario_creacion else 'Sistema'}
        """
        
        if self.proximo_envio:
            mensaje += f"\n*Próximo recordatorio*: {self.proximo_envio.strftime('%d/%m/%Y %H:%M')}"
        
        try:
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': settings.TELEGRAM_CHAT_ID,
                'text': mensaje,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            response = requests.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            # Registrar el error en logs
            from django.core import mail
            mail.mail_admins(
                subject=f"Error enviando Telegram de seguimiento {self.id}",
                message=f"Error: {str(e)}"
            )
    
    def save(self, *args, **kwargs):
        # Calcular próxima fecha de envío si no está definida
        if not self.proximo_envio and self.frecuencia_envio and self.hora_envio:
            self.proximo_envio = self.calcular_proximo_envio()
            
        # Si se marca para enviar ahora, establecer próxima fecha como ahora
        if self.enviar_ahora:
            self.proximo_envio = timezone.now()
            
        super().save(*args, **kwargs)
        
        # Si es un nuevo registro y está marcado para enviar ahora, enviar inmediatamente
        if kwargs.get('created', False) and self.enviar_ahora:
            self.enviar_notificaciones()

# Señal para manejar notificaciones después de guardar
@receiver(post_save, sender=SeguimientoAlertas)
def manejar_notificaciones(sender, instance, created, **kwargs):
    if created and instance.enviar_notificacion and not instance.enviar_ahora:
        instance.enviar_notificaciones()