from rest_framework import serializers
from .models import Newsletter

class NewsletterSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()
    autor_username = serializers.CharField(source='autor.username', read_only=True)

    class Meta:
        model = Newsletter
        fields = [
            'id', 'titulo', 'contenido', 'imagen_url', 
            'created_at', 'autor', 'autor_username', 'is_published'
        ]
        read_only_fields = ['autor']  # El autor se asigna automáticamente

    def get_imagen_url(self, obj):
        if obj.imagen:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.imagen.url)  # Corregido: obj.imagen.url (no obj.img.url)
        return None