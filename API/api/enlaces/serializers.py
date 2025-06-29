from rest_framework import serializers
from .models import *

class EnlaceSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Enlace
        fields = "__all__"
        
    def get_imagen_url(self, obj):
        if obj.imagen:
            return obj.imagen.url
        return None