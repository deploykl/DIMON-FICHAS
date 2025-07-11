from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser

from api.Choises import GENDER_CHOICES 

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d',default='img/empty.png', null = True, blank = True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Género", null=True, blank=True)
    password_reset_token = models.CharField(max_length=50, null=True, blank=True)
    password_reset_token_expires = models.DateTimeField(null=True, blank=True)
    telegram_chat_id = models.BigIntegerField(verbose_name="ID de Chat de Telegram",null=True,blank=True, unique=True,)
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
    