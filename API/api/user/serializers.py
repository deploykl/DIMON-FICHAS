from .models import *
from rest_framework import serializers

# Create your views here.
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    dependencia_name = serializers.ReadOnlyField(source="dependencia.name")
    area_name = serializers.ReadOnlyField(source="area.name")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "password2",
            "image",
            "dependencia_name",
            "is_superuser",
            "area_name",
        ]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password2": "Las contraseñas no coinciden"}
            )

        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError(
                {"username": "Este nombre de usuario ya está en uso"}
            )

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                {"email": "Este correo electrónico ya está en uso"}
            )

        return data

    def create(self, validated_data):
        validated_data.pop(
            "password2"
        )  # Eliminar la confirmación de contraseña antes de crear el usuario
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class ConsultaExternaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultaExterna
        fields = '__all__'
        read_only_fields = ('creado_por', 'fecha_creacion', 'fecha_actualizacion')
        
class CirugiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cirugia
        fields = '__all__'
        read_only_fields = ('creado_por', 'fecha_creacion', 'fecha_actualizacion')