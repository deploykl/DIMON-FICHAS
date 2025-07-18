from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('image', 'genero', 'telegram_chat_id' , 'access_ConsultaExterna', 'codigo', 'nombre', 'distrito', 'disa', 'categoria'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'genero', 'is_staff')
    list_filter = ('genero', 'is_staff', 'is_superuser')
