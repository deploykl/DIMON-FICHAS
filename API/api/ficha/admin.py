from django.contrib import admin
from .models import Categoria, Proceso, Subproceso, Verificador, EvaluacionVerificador

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'tipo')
    search_fields = ('name', 'tipo')
    list_filter = ('tipo',)

class ProcesoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'nombre_proceso', 'dueño_proceso')
    search_fields = ('nombre', 'nombre_proceso', 'dueño_proceso')
    list_filter = ('categoria',)
    raw_id_fields = ('categoria',)

class SubprocesoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'proceso', 'nivel')
    search_fields = ('nombre', 'proceso__nombre')
    list_filter = ('nivel', 'proceso__categoria')
    raw_id_fields = ('proceso',)

class VerificadorAdmin(admin.ModelAdmin):
    list_display = ('subproceso', 'descripcion_short', 'orden')
    search_fields = ('descripcion', 'subproceso__nombre')
    list_filter = ('subproceso__proceso__categoria',)
    ordering = ('orden',)
    
    def descripcion_short(self, obj):
        return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_short.short_description = 'Descripción'

class EvaluacionVerificadorAdmin(admin.ModelAdmin):
    list_display = ('verificador', 'establecimiento', 'estado_display', 'usuario', 'fecha_evaluacion')
    search_fields = ('verificador__descripcion', 'establecimiento', 'codigo')
    list_filter = ('estado', 'tipo', 'usuario')
    date_hierarchy = 'fecha_evaluacion'
    readonly_fields = ('fecha_evaluacion',)
    
    def estado_display(self, obj):
        return obj.get_estado_display()
    estado_display.short_description = 'Estado'
    
    fieldsets = (
        ('Información de la Evaluación', {
            'fields': ('usuario', 'fecha_evaluacion', 'estado', 'observaciones')
        }),
        ('Datos del Verificador', {
            'fields': ('verificador',)
        }),
        ('Datos de la IPRESS', {
            'fields': ('establecimiento', 'tipo', 'codigo', 'categoria')
        }),
    )

# Registro de modelos
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Proceso, ProcesoAdmin)
admin.site.register(Subproceso, SubprocesoAdmin)
admin.site.register(Verificador, VerificadorAdmin)
admin.site.register(EvaluacionVerificador, EvaluacionVerificadorAdmin)