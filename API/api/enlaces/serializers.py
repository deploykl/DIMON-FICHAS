from rest_framework import serializers
from .models import *

class EnlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enlace
        fields = "__all__"