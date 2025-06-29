from django.db import models

class Enlace(models.Model):
    titulo = models.CharField(max_length=500, verbose_name="Título")
    url = models.URLField(max_length=2000, verbose_name="URL")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    def __str__(self):
        return f"{self.titulo} - {self.url}"

    class Meta:
        verbose_name = "Enlace"
        verbose_name_plural = "Enlaces"
        ordering = ['-fecha_creacion']