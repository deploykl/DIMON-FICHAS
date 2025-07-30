from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import datetime
from api.Choises import GENDER_CHOICES


# Create your models here.
class User(AbstractUser):
    image = models.ImageField(
        upload_to="users/%Y/%m/%d", default="img/empty.png", null=True, blank=True
    )
    genero = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Género",
        null=True,
        blank=True,
    )
    password_reset_token = models.CharField(max_length=50, null=True, blank=True)
    password_reset_token_expires = models.DateTimeField(null=True, blank=True)
    telegram_chat_id = models.BigIntegerField(
        verbose_name="ID de Chat de Telegram",
        null=True,
        blank=True,
        unique=True,
    )

    access_ConsultaExterna = models.BooleanField(default=False)
    codigo = models.CharField(null=True, blank=True, max_length=8)
    nombre = models.CharField(null=True, blank=True, max_length=200)
    distrito = models.CharField(null=True, blank=True, max_length=100)
    disa = models.CharField(null=True, blank=True, max_length=100)
    categoria = models.CharField(null=True, blank=True, max_length=20)

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
    n_hcl = models.CharField(max_length=20, verbose_name="Número de Historia Clínica")
    fecha_hora_cita_otorgada = models.DateTimeField()
    fecha_hora_atencion = models.DateTimeField()
    diagnostico_medico = models.TextField()
    dx_CIE_10_1 = models.CharField(
        max_length=10, verbose_name="Diagnóstico CIE-10 Principal"
    )
    dx_CIE_10_2 = models.CharField(
        max_length=10,
        verbose_name="Diagnóstico CIE-10 Secundario",
        blank=True,
        null=True,
    )
    dx_CIE_10_3 = models.CharField(
        max_length=10,
        verbose_name="Diagnóstico CIE-10 Terciario",
        blank=True,
        null=True,
    )
    especialidad = models.CharField(max_length=100)
    creado_por = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="consultas_creadas"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Consulta {self.id} - {self.documento} - {self.fecha_hora_atencion.date()}"
        )

    def clean(self):
        super().clean()
        # Validar campos requeridos
        required_fields = {
            "tipo_seguro": "El tipo de seguro es obligatorio",
            "fecha_nacimiento": "La fecha de nacimiento es obligatoria",
            "sexo": "El sexo es obligatorio",
            "lugar_procedencia": "El lugar de procedencia es obligatorio",
            "n_hcl": "El número de historia clínica es obligatorio",
            "fecha_hora_cita_otorgada": "La fecha/hora de cita otorgada es obligatoria",
            "fecha_hora_atencion": "La fecha/hora de atención es obligatoria",
            "diagnostico_medico": "El diagnóstico médico es obligatorio",
            "dx_CIE_10_1": "El diagnóstico CIE-10 principal es obligatorio",
            "especialidad": "La especialidad es obligatoria",
        }

        for field, error_msg in required_fields.items():
            if not getattr(self, field):
                raise ValidationError({field: error_msg})

        # Validación adicional para fechas
        if self.fecha_hora_cita_otorgada and self.fecha_hora_atencion:
            if self.fecha_hora_atencion < self.fecha_hora_cita_otorgada:
                raise ValidationError(
                    "La fecha de atención no puede ser anterior a la fecha de cita otorgada"
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Cirugia(models.Model):
    tipo_seguro = models.CharField(max_length=70)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=GENDER_CHOICES)
    lugar_procedencia = models.CharField(max_length=100)
    n_hcl = models.CharField(max_length=20, verbose_name="Número de Historia Clínica")
    fecha_iqx_programada = models.DateTimeField()
    codigo_iqx_programada = models.CharField(max_length=100)
    iqx_programada = models.CharField(max_length=100)
    fecha_iqx_realizada = models.DateTimeField()
    codigo_iqx_realizada = models.CharField(max_length=100)
    iqx_realizada = models.CharField(max_length=100)
    se_reprogramo = models.CharField(max_length=100)
    fecha_iqx_reprogramada = models.DateTimeField()
    motivo_reprogramacion = models.CharField(
        max_length=255, null=True, blank=True
    )  # <- Correcto
    fecha_realizada_iqx_reprogramada = models.DateTimeField()
    codigo_iqx_reprogramada = models.CharField(max_length=100)
    iqx_reprogramada = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="cirugias"
    )

    def __str__(self):
        return f"Cirugía {self.id} - {self.iqx_programada} - {self.fecha_iqx_programada.date()}"

    def clean(self):
        # Validación 1: si se reprogramó
        if self.se_reprogramo and self.se_reprogramo.upper() == "SI":
            required_fields = [
                "fecha_iqx_reprogramada",
                "motivo_reprogramacion",
                "fecha_realizada_iqx_reprogramada",
                "codigo_iqx_reprogramada",
                "iqx_reprogramada",
            ]
            for field in required_fields:
                if not getattr(self, field):
                    raise ValidationError(
                        {
                            field: f"El campo '{field}' es requerido cuando se_reprogramo es 'SI'"
                        }
                    )

        # Validación 2: fecha mínima
        if (
            self.fecha_iqx_realizada
            and self.fecha_iqx_realizada.date() < datetime(2025, 3, 1).date()
        ):
            raise ValidationError(
                {
                    "fecha_iqx_realizada": "La fecha de cita debe ser a partir del 1 de marzo de 2025."
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # ejecuta `clean` automáticamente
        super().save(*args, **kwargs)
