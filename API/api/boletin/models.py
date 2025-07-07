from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Newsletter(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(
        upload_to='newsletters/img/',
        blank=True,
        null=True,
        help_text="Imagen destacada del boletín"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='newsletters')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-created_at']  # Ordenar por fecha descendente