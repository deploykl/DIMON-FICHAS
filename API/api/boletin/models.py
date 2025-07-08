from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()

class Newsletter(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='newsletters')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-created_at']
        
class NewsletterImage(models.Model):
    newsletter = models.ForeignKey(
        Newsletter, 
        on_delete=models.CASCADE,
        related_name='imagenes'
    )
    imagen = models.ImageField(
        upload_to='newsletters/img/%Y/%m/%d/',  # Mejor organización por fecha
        help_text="Imagen del boletín (formatos: JPG, PNG, GIF)",
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]  # Validar tipos de archivo
    )
    orden = models.PositiveIntegerField(
        default=0,
        help_text="Orden de visualización (0=primero)"
    )
    es_portada = models.BooleanField(
        default=False,
        help_text="¿Es la imagen principal/portada del boletín?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Para trackear modificaciones

    class Meta:
        ordering = ['orden', 'created_at']
        verbose_name = 'Imagen de boletín'
        verbose_name_plural = 'Imágenes de boletines'
        constraints = [
            # Asegura que solo haya una imagen como portada por boletín
            models.UniqueConstraint(
                fields=['newsletter', 'es_portada'],
                condition=models.Q(es_portada=True),
                name='unique_portada_por_newsletter'
            )
        ]

    def __str__(self):
        return f"Imagen #{self.orden} para {self.newsletter.titulo}"

    def save(self, *args, **kwargs):
        # Si se marca como portada, desmarcar otras portadas del mismo boletín
        if self.es_portada:
            NewsletterImage.objects.filter(
                newsletter=self.newsletter, 
                es_portada=True
            ).exclude(pk=self.pk).update(es_portada=False)
        super().save(*args, **kwargs)