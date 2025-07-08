from rest_framework import serializers
from .models import Newsletter, NewsletterImage

class NewsletterImageSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()
    es_portada = serializers.BooleanField(required=False)  # Añadir este campo

    class Meta:
        model = NewsletterImage
        fields = ['id', 'imagen_url', 'orden', 'es_portada', 'imagen']  # Añadir 'imagen' y 'es_portada'
        read_only_fields = ['id', 'imagen_url']

    def get_imagen_url(self, obj):
        if obj.imagen:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.imagen.url)
        return None

class NewsletterSerializer(serializers.ModelSerializer):
    imagenes = NewsletterImageSerializer(many=True, read_only=True)
    autor_username = serializers.CharField(source='autor.username', read_only=True)
    imagen_principal_url = serializers.SerializerMethodField()

    class Meta:
        model = Newsletter
        fields = [
            'id', 'titulo', 'contenido', 'imagen_principal_url', 
            'created_at', 'autor', 'autor_username', 'is_published',
            'imagenes'
        ]
        read_only_fields = ['autor']

    def get_imagen_principal_url(self, obj):
        # Devuelve la URL de la primera imagen si existe
        if obj.imagenes.exists():
            request = self.context.get('request')
            first_image = obj.imagenes.first()
            return request.build_absolute_uri(first_image.imagen.url)
        return None