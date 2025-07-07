from django.contrib import admin

from api.boletin.models import Newsletter

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'created_at', 'is_published')
    search_fields = ('titulo', 'contenido')
    list_filter = ('is_published', 'autor')