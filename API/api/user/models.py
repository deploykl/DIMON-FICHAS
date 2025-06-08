from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser

from api.Choises import GENDER_CHOICES 

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d',default='img/empty.png', null = True, blank = True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Género", null=True, blank=True)

    def delete(self, *args, **kwargs):
        try:
            super().delete(*args, **kwargs)
        except IntegrityError as e:
            print(f"Error al eliminar usuario: {e}")
            # Puedes lanzar la excepción de nuevo si quieres manejarla en otra parte
            raise